import re
import sys
import xml.etree.ElementTree as et

from siepic_forge._layers import _layers

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError(
            "Please run the script providing the path for the waveguide files directory: WAVEGUIDES*.xml"
        )

    tree = et.parse(sys.argv[1])
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
            layer_name = component.find("layer").text
            if "Si - 90 nm etch" == layer_name:
                layer_name = "Si Slab"
            layer = _layers[layer_name].layer
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
            num_modes = (2 if "TE" in name else 1) if "TM" in name else 1
            added_solver_modes = (0 if "TE" in name else 1) if "TM" in name else 0
            polarization = '"TM"' if added_solver_modes > 0 else None
            if name.startswith("MM_"):
                added_solver_modes = 0
                if name.endswith("_3000"):
                    num_modes = 7 if "SiN" in name else 17
                elif name.endswith("_2000"):
                    num_modes = 12
                else:
                    raise RuntimeError("Unrecognized MM waveguide.")
        print(f"""{name!r}: pf.PortSpec(
    description={desc!r},
    width={0.5 + width},
    limits=(-1, 1 + {limit_layer}_thickness),
    num_modes={num_modes},
    added_solver_modes={added_solver_modes},
    polarization={polarization},
    target_neff={target_neff},
    path_profiles={tuple(path_profiles)},
),""")
