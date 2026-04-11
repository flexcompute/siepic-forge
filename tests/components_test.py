import siepic_forge as siepic

from siepic_forge.component import _component_data


def test_components():
    technology = (siepic.ebeam_si(), siepic.ebeam_sin())
    for name in siepic.component_names:
        i = 1 if "SiN" in _component_data[name][0] else 0
        _ = siepic.component(name, technology=technology[i])
