import photonforge as pf
import siepic_forge as siepic


def test_export(tmp_path):
    tech = siepic.ebeam()
    tech_file = tmp_path / "tech.json"
    tech.write_json(tech_file)
    tech_loaded = pf.Technology.load_json(tech_file)
    assert tech_loaded.name == tech.name
    assert tech_loaded.version == tech.version
    assert tech_loaded.layers == tech.layers
    assert tech_loaded.ports == tech.ports
    assert tech_loaded.extrusion_specs == tech.extrusion_specs
    assert tech_loaded.background_medium == tech.background_medium
    assert tech_loaded == tech

