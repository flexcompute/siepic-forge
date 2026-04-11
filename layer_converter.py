import pathlib
import subprocess
import sys
import xml.etree.ElementTree as et


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


def parse(layers, node, description=""):
    layer = node.find("source").text
    if layer == "*/*":
        return
    i = layer.find("/")
    j = i + layer[i:].find("@")
    layer = (int(layer[:i]), int(layer[i + 1 : j]))

    name = node.find("name").text
    color = node.find("fill-color").text + "18"

    key = prop.find("dither-pattern").text
    key = layer if key is None else key[1:]
    pattern = patterns.get(key, "")

    if layer in layers:
        other = layers[layer]
        if len(description) == 0:
            description = other[2]
        elif len(other[2]) > 0 and other[2] != description:
            description += f"/{other[2]}"
        if len(other[0]) < len(name):
            if len(description) == 0:
                description = name
            name = other[0]
            color = other[3]
            pattern = other[4]
        else:
            if len(description) == 0:
                description = other[0]
    layers[layer] = [name, layer, description, color, pattern]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError(
            "Please run the script providing the path for the layer properties file: EBeam.lyp"
        )

    layers = {}

    tree = et.parse(sys.argv[1])
    root = tree.getroot()
    for prop in root.findall("properties"):
        name = prop.find("name").text.strip()
        members = prop.findall("group-members")
        if len(members) > 0:
            for member in members:
                parse(layers, member, name)
        else:
            parse(layers, prop)

    for n, name in (
        ((1, 0), "Si"),
        ((2, 0), "Si Slab"),
        ((4, 0), "SiN"),
        ((10, 0), "Text"),
        ((11, 0), "M1_heater"),
        ((12, 0), "M2_router"),
        ((13, 0), "M_Open"),
    ):
        layer = layers[n]
        if len(layer[2]) == 0:
            layer[2] = layer[0]
        else:
            layer[2] = f"{layer[2]} - {layer[0]}"
        layer[0] = name

    names = {n: 0 for n, *_ in layers.values()}
    for k in sorted(layers):
        n = layers[k][0]
        if names[n] > 0:
            layers[k][0] = f"{n} {names[n]}"
        names[n] += 1

    lines = [
        "import photonforge as pf",
        "_layers = {",
    ] + [
        "\t{!r} : pf.LayerSpec({}, {!r}, {!r}, {!r}),".format(*v) for _, v in sorted(layers.items())
    ]
    lines.append("}")

    output = pathlib.Path(__file__).parent / "siepic_forge" / "_layers.py"
    output.write_text("\n".join(lines))
    subprocess.run(["ruff", "format", output], check=True)
