import pathlib
import subprocess
import sys

import numpy
import photonforge as pf

sys.path.append("./si")
sys.path.append("./sin")

import siepic_si_forge as siepic_si
import siepic_sin_forge as siepic_sin

preambles = {
    "si": """import math

_symmetries_3port = [("P1", "P2", {"P0": "P0", "P2": "P1"})]

_symmetries_crossing = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P1", "P3": "P0"}),
    ("P0", "P3", {"P1": "P2", "P2": "P0", "P3": "P1"}),
]

_waist = 5.0

_angle = 8 * math.pi / 180
_vx8 = math.sin(_angle)
_vy8 = -math.cos(_angle)

_angle = 7 * math.pi / 180
_tm1550_vx = math.sin(_angle)
_tm1550_vy = -math.cos(_angle)

_angle = -21 * math.pi / 180
_te1550_vx = math.sin(_angle)
_te1550_vy = -math.cos(_angle)

_component_data = {
""",
    "sin": """import math

_symmetries_3port = [("P1", "P2", {"P0": "P0", "P2": "P1"})]

_symmetries_crossing = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P2", "P3", {"P0": "P1", "P1": "P0", "P3": "P2"}),
]

_symmetries_directional_coupler = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P0", "P3": "P1"}),
    ("P0", "P3", {"P1": "P2", "P2": "P1", "P3": "P0"}),
]

_symmetries_mmi22 = _symmetries_directional_coupler

_waist = 5.0

_angle = 8 * math.pi / 180
_vx8 = math.sin(_angle)
_vy8 = -math.cos(_angle)

_angle = 10 * math.pi / 180
_te895_vx = math.sin(_angle)
_te895_vy = -math.cos(_angle)

_component_data = {
""",
}

for family, preamble in preambles.items():
    lines = []
    technology = siepic_sin.ebeam() if family == "sin" else siepic_si.ebeam()
    path = pathlib.Path(f"{family}/siepic_{family}_forge/library")
    for gds_name in sorted(path.glob("*.gds")):
        components = pf.load_layout(gds_name, technology=technology)
        for comp_name in sorted(c.name for c in pf.find_top_level(*components.values())):
            comp = components[comp_name]
            if comp.name[0] == "$":
                continue
            comp.remap_layers({(1, 99): (1, 0)})
            fibers = [
                tuple(float(x) for x in numpy.round((s.x_mid, s.y_mid), decimals=3))
                for s in comp.structures.get((81, 0), [])
            ]
            pins = [
                numpy.round((s.x_mid, s.y_mid), decimals=3)
                for s in comp.structures.get((1, 10), [])
            ]
            ports = []
            for pin in pins:
                candidates = []
                for spec in technology.ports:
                    for port in comp.detect_ports([spec], (pin - 0.005, pin + 0.005)):
                        if numpy.allclose(port.center, pin):
                            candidates.append(
                                (tuple(float(x) for x in pin), int(port.input_direction), spec)
                            )
                if len(candidates) == 0:
                    print(f"# WARN: Missing port {tuple(float(x) for x in pin)}.")
                ports.extend(candidates)
            ports.extend((tuple(c),) for c in fibers)

            ports = ", ".join(repr(p) for p in ports)

            model = "None" if len(ports) < 2 or comp.name.endswith("BB") else "{}"

            lines.append(f"{comp.name!r}: ({gds_name.stem!r}, [{ports}], {model}),")

    output = pathlib.Path(__file__).parent / family / f"siepic_{family}_forge" / "_component_data.py"
    output.write_text(preamble + "\n".join(lines) + "\n}")
    subprocess.run(["ruff", "format", output], check=True)
