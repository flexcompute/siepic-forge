import inspect
import pathlib
import subprocess

import tidy3d as td
from tidy3d.material_library.material_library import MaterialItem

import photonforge as pf
import siepic_forge as siepic


mat_lib = {}
for name, mi in td.material_library.items():
    if not isinstance(mi, MaterialItem):
        continue
    for spec, var in mi.variants.items():
        if not isinstance(var.medium, td.components.medium.MediumType):
            continue
        mat_lib[var.medium] = {
            "type": "material_library",
            "value": {"path": [name, spec]},
        }


pf.config.svg_labels = False
pf.config.svg_port_names = False
pf.config.default_technology = siepic.ebeam()

components = []
for name in sorted(siepic.component_names):
    c = siepic.component(name)
    svg = c._repr_svg_()
    components.append(
        {
            "arguments": [
                {
                    "name": "technology",
                    "placeholder": "Use the global default technology.",
                    "required": False,
                    "tooltip": "Component technology.",
                    "type": "technology",
                }
            ],
            "hiddenArguments": {"cell_name": name},
            "function": "component",
            "label": name.replace("_", " "),
            "svg": svg,
        }
    )


replacements = {
    "Sin": "Si₃N₄",
    "Sio2": "SiO₂",
}


def make_label(name):
    if name.startswith("loca_i"):
        name = "LoCA-i" + name[6:]
    elif name.startswith("loca_s"):
        name = "LoCA-s" + name[6:]
    words = name.replace("_", " ").title().split()
    return " ".join(replacements.get(w, w) for w in words)


def process(name, value, tooltip):
    arg = {
        "defaults": value,
        "label": make_label(name),
        "name": name,
        "tooltip": tooltip,
    }
    if name == "metal_layers":
        arg = {
            "defaults": 2,
            "label": "Metal Layers",
            "name": "metal_layers",
            "options": [2, 4],
            "type": "select",
            "tooltip": "Number of metal layers (2 or 4).",
        }
    elif isinstance(value, bool):
        arg["type"] = "checkbox"
    elif isinstance(value, (float, int)):
        arg["type"] = "number"
        if "angle" in name:
            arg["suffix"] = "°"
            arg["validates"] = ["exclusiveMin", "exclusiveMax"]
            arg["validatesArgs"] = {"exclusiveMin": [-90], "exclusiveMax": [90]}
        else:
            arg["suffix"] = "μm"
            if any(w in name for w in ("thickness", "depth", "separation", "gap")):
                arg["validates"] = ["exclusiveMin"]
                arg["validatesArgs"] = {"exclusiveMin": [0]}
    elif isinstance(value, siepic.technology._Medium):
        arg["type"] = "medium"
        d = value.dict()
        if value in mat_lib:
            arg["defaults"] = mat_lib[value]
        else:
            arg["defaults"] = {
                "type": "constructor",
                "value": {n: d[n] for n in ("type",) + tuple(value.__fields_set__)},
            }
            if "poles" in arg["defaults"]["value"]:
                arg["defaults"]["value"]["poles"] = tuple(
                    ({"real": a.real, "imag": a.imag}, {"real": b.real, "imag": b.imag})
                    for a, b in arg["defaults"]["value"]["poles"]
                )
    elif isinstance(value, dict) and all(
        isinstance(v, siepic.technology._Medium) for v in value.values()
    ):
        children = []
        for k, v in value.items():
            child = {
                "type": "medium",
                "name": k,
                "hideLabel": True,
                "prefix": k.title(),
            }
            d = v.dict()
            if v in mat_lib:
                child["defaults"] = mat_lib[v]
            else:
                child["defaults"] = {
                    "type": "constructor",
                    "value": {n: d[n] for n in ("type",) + tuple(v.__fields_set__)},
                }
                if "poles" in child["defaults"]["value"]:
                    child["defaults"]["value"]["poles"] = tuple(
                        ({"real": a.real, "imag": a.imag}, {"real": b.real, "imag": b.imag})
                        for a, b in child["defaults"]["value"]["poles"]
                    )
            children.append(child)
        arg = {
            "itemSpan": 24,
            "label": make_label(name),
            "name": name,
            "tooltip": tooltip,
            "type": "subForm",
            "children": children,
        }
    return arg


technologies = []
for tech in (siepic.ebeam,):
    parameters = inspect.signature(tech).parameters

    args = []
    go_args = False
    name = None
    tooltip = None

    for line in tech.__doc__.splitlines():
        if go_args:
            if len(line.strip()) == 0:
                args.append(process(name, parameters[name].default, tooltip))
                break
            if line.startswith("      "):
                tooltip += " " + line.strip()
            else:
                if name:
                    args.append(process(name, parameters[name].default, tooltip))
                name = line[4 : 4 + line[4:].find(" (")]
                tooltip = line[line.find(":") + 2 :]
        else:
            go_args = line.strip() == "Args:"
    technologies.append(
        {
            "arguments": args,
            "function": tech.__name__,
            "label": pf.config.default_technology.name,
        }
    )

json = {"components": components, "technologies": technologies}

pathlib.Path("siepic_forge/_ui_.py").write_text("json = " + repr(json))
subprocess.run(["black", "-C", "--fast", "siepic_forge/_ui_.py"])
