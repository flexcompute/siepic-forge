import siepic_forge as siepic


def test_components():
    technology = siepic.ebeam()
    for name in siepic.component_names:
        _ = siepic.component(name, technology=technology)
