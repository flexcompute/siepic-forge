import photonforge as pf
import siepic_forge as siepic
import pathlib
import numpy


pf.config.default_technology = siepic.ebeam()

for path in pathlib.Path("siepic_forge/library").iterdir():
    family = path.stem
    for gds_name in sorted(path.glob("*.gds")):
        components = pf.load_layout(gds_name)
        for comp_name in sorted(c.name for c in pf.find_top_level(*components.values())):
            comp = components[comp_name]
            if comp.name[0] == "$":
                continue
            pins = []
            for s in comp.structures:
                if s.layer == (1, 99):
                    s.layer = (1, 0)
                elif s.layer == (1, 10):
                    center = numpy.round((s.x_mid, s.y_mid), decimals=3)
                    pins.append(center)
            ports = []
            for pin in pins:
                candidates = []
                for spec in pf.config.default_technology.ports:
                    for port in comp.detect_ports([spec], (pin - 0.005, pin + 0.005)):
                        if numpy.allclose(port.center, pin):
                            candidates.append((tuple(pin), int(port.input_direction), spec))
                if len(candidates) == 0:
                    print(f"# WARN: Missing port {tuple(pin)}.")
                ports.extend(candidates)

            sym = {
                2: "_symmetries_2port",
                3: "_symmetries_3port",
                4: "_symmetries_directional_coupler",
            }.get(len(ports), "[]")
            model = (
                "None" if len(ports) < 2 else '(pf.Tidy3DModel, {"port_symmetries": ' + sym + "})"
            )

            ports = ", ".join(repr(p) for p in ports)

            print(
                f"""{comp.name!r}: (
    {family!r},
    {gds_name.stem!r},
    [{ports}],
    {model},
),"""
            )
