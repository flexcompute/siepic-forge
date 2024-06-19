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
            comp.remap_layers({(1, 99): (1, 0)})
            fibers = [
                numpy.round((s.x_mid, s.y_mid), decimals=3)
                for s in comp.structures.get((81, 0), [])
            ]
            pins = [
                numpy.round((s.x_mid, s.y_mid), decimals=3)
                for s in comp.structures.get((1, 10), [])
            ]
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
            ports.extend((tuple(c),) for c in fibers)

            ports = ", ".join(repr(p) for p in ports)

            model = "None" if len(ports) < 2 else "(pf.Tidy3DModel, {})"

            print(
                f"""{comp.name!r}: (
    {family!r},
    {gds_name.stem!r},
    [{ports}],
    {model},
),"""
            )
