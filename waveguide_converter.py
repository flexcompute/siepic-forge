import xml.etree.ElementTree as et
import re


pdk = "/home/lucas/Flexcompute/pdk/SiEPIC_EBeam_PDK/klayout/EBeam"

layers = {
    "Waveguide": ((1, 99), "Waveguides", "#ff80a818", "\\"),
    "Si": ((1, 0), "Waveguides", "#ff80a818", "\\\\"),
    "SiN": ((1, 5), "Waveguides", "#a6cee318", "\\\\"),
    "Si - 90 nm rib": ((2, 0), "Waveguides", "#80a8ff18", "/"),
    "Si_Litho193nm": ((1, 69), "Waveguides", "#cc80a818", "\\"),
    "Oxide open (to BOX)": ((6, 0), "Waveguides", "#ffae0018", "\\"),
    "Text": ((10, 0), "", "#0000ff18", "\\"),
    "Si N": ((20, 0), "Doping", "#7000FF18", "\\\\"),
    "Si N++": ((24, 0), "Doping", "#0000ff18", ":"),
    "M1_heater": ((11, 0), "Metal", "#ebc63418", "xx"),
    "M2_router": ((12, 0), "Metal", "#3471eb18", "xx"),
    "M_Open": ((13, 0), "Metal", "#00000018", "xx"),
    "VC": ((40, 0), "Metal", "#3a027f18", "xx"),
    "FloorPlan": ((99, 0), "Misc", "#8000ff18", "hollow"),
    "Deep Trench": ((201, 0), "Misc", "#c0c0c018", "solid"),
    "Dicing": ((210, 0), "Misc", "#a0a0c018", "solid"),
    "Chip design area": ((290, 0), "Misc", "#80005718", "hollow"),
    "Keep out": ((202, 0), "Misc", "#a0a0c018", "//"),
    "SEM": ((200, 0), "Misc", "#ff00ff18", "\\"),
    "DevRec": ((68, 0), "SiEPIC", "#00408018", "hollow"),
    "PinRec": ((1, 10), "SiEPIC", "#00408018", "/"),
    "PinRecM": ((1, 11), "SiEPIC", "#00408018", "/"),
    "FbrTgt": ((81, 0), "SiEPIC", "#00408018", "/"),
    "Errors": ((999, 0), "SiEPIC", "#00008018", "/"),
    "Lumerical": ((733, 0), "SiEPIC", "#80005718", "hollow"),
    "BlackBox": ((998, 0), "SiEPIC", "#00408018", "solid"),
}

for name in ("WAVEGUIDES.xml", "WAVEGUIDES_SiN.xml"):
    tree = et.parse(f"{pdk}/{name}")
    root = tree.getroot()
    for prop in root.findall("waveguide"):
        desc = prop.find("name").text

        name = ""
        remaining = desc
        if remaining.startswith("Multimode "):
            name += "MM_"
            remaining = remaining[10:]
        if remaining.startswith("Strip "):
            remaining = remaining[6:]
        else:
            i = remaining.find(" ")
            name += remaining[:i] + "_"
            remaining = remaining[i + 1 :]
        i = remaining.find("TE-TM")
        n = 5
        if i < 0:
            i = remaining.find("TE")
            n = 2
        if i < 0:
            i = remaining.find("TM")
        if i >= 0:
            name += remaining[i : i + n]
        match = re.search(r"[^=](\d{3,4})", remaining[i + n :])
        if match:
            name += "_" + match.groups(1)[0]
        match = re.search(r"w=(\d*) nm", remaining[i + n :])
        if match:
            name += "_" + match.groups(1)[0]

        path_profiles = []
        dev_rec_width = 0
        for component in prop.findall("component"):
            width = float(component.find("width").text)
            offset = float(component.find("offset").text)
            layer = layers[component.find("layer").text][0]
            if layer == (68, 0):
                dev_rec_width = width
                continue
            elif layer == (1, 99):
                continue
            path_profiles.append((width, offset, layer))
        if len(path_profiles):
            width = dev_rec_width if dev_rec_width > 0 else float(prop.find("width").text) + 2.0
            target_neff = 2.1 if "SiN" in name else 3.5
            limit_layer = "sin" if "SiN" in name else "si"
            num_modes = 2 if "TM" in name else 1
            if name.startswith("MM_"):
                if name.endswith("_3000"):
                    num_modes = 14
                elif name.endswith("_2000"):
                    num_modes = 10
                else:
                    raise RuntimeError("Unrecognized MM waveguide.")
            print(
                f"""{name!r}: pf.PortSpec(
    description={desc!r},
    width={width},
    limits=(-1.5, 1.5 + {limit_layer}_thickness),
    num_modes={num_modes},
    target_neff={target_neff},
    path_profiles={tuple(path_profiles)},
),"""
            )
