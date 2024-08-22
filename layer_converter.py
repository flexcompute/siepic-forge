import xml.etree.ElementTree as et


pdk = "/home/lucas/Flexcompute/pdk/SiEPIC_EBeam_PDK/klayout/EBeam"


def hex_to_rgba(color):
    "Convert a hex string to RGBA color components"

    if not isinstance(color, str) or len(color) == 0:
        raise TypeError("Argument must be a valid string.")

    if color[0] == "#":
        color = color[1:]

    n = len(color)
    if n == 3:  # "RGB"
        return tuple(int(c * 2, 16) for c in color) + (255,)
    if n == 4:  # "RGBA"
        return tuple(int(c * 2, 16) for c in color)
    if n == 6:  # "RRGGBB"
        return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4)) + (255,)
    if n == 8:  # "RRGGBBAA"
        return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4, 6))
    raise ValueError("Argument not recognized as a hex-valued RGBA color.")


# Klayout patterns
patterns = {
    "0": "solid",  # solid
    "1": "hollow",  # hollow
    "2": ":",  # dotted
    "3": ".",  # coarsely dotted
    "4": "\\\\",  # left-hatched
    "5": "\\",  # lightly left-hatched
    "6": "\\\\",  # strongly left-hatched dense
    "7": "\\",  # strongly left-hatched sparse
    "8": "//",  # right-hatched
    "9": "/",  # lightly right-hatched
    "10": "//",  # strongly right-hatched dense
    "11": "/",  # strongly right-hatched sparse
    "12": "xx",  # cross-hatched
    "13": "x",  # lightly cross-hatched
    "14": "+",  # checkerboard 2px
    "15": "x",  # strongly cross-hatched sparse
    "16": "xx",  # heavy checkerboard
    "17": "x",  # hollow bubbles
    "18": "x",  # solid bubbles
    "19": "+",  # pyramids
    "20": "+",  # turned pyramids
    "21": "+",  # plus
    "22": "-",  # minus
    "23": "/",  # 22.5 degree down
    "24": "\\",  # 22.5 degree up
    "25": "//",  # 67.5 degree down
    "26": "\\\\",  # 67.5 degree up
    "27": "x",  # 22.5 cross hatched
    "28": "x",  # zig zag
    "29": "x",  # sine
    "30": "+",  # special pattern for light heavy dithering
    "31": "+",  # special pattern for light frame dithering
    "32": "||",  # vertical dense
    "33": "|",  # vertical
    "34": "||",  # vertical thick
    "35": "|",  # vertical sparse
    "36": "|",  # vertical sparse, thick
    "37": "=",  # horizontal dense
    "38": "-",  # horizontal
    "39": "=",  # horizontal thick
    "40": "-",  # horizontal
    "41": "-",  # horizontal
    "42": "++",  # grid dense
    "43": "+",  # grid
    "44": "++",  # grid thick
    "45": "+",  # grid sparse
    "46": "+",  # grid sparse, thick
}


def parse(node, group=""):
    name = node.find("name").text
    if name == "Si - 90 nm rib":
        name = "Si slab"
    elif name == "Lumerical":
        name = "FDTD"
    layer = node.find("source").text
    i = layer.find("/")
    j = i + layer[i:].find("@")
    layer = (int(layer[:i]), int(layer[i + 1 : j]))
    color = node.find("fill-color").text + "18"
    pattern = patterns[node.find("dither-pattern").text[1:]]
    print(f"{name!r}: pf.LayerSpec({layer}, {group!r}, {color!r}, {pattern!r}),")


tree = et.parse(f"{pdk}/EBeam.lyp")
root = tree.getroot()
for prop in root.findall("properties"):
    name = prop.find("name").text
    members = prop.findall("group-members")
    if len(members) > 0:
        for member in members:
            parse(member, name)
    else:
        parse(prop)
