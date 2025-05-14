import inspect
import json
import siepic_forge as siepic
from siepic_forge import _ui_


def test_ui_technologies():
    assert len(_ui_.json["technologies"]) > 0
    for tech in _ui_.json["technologies"]:
        assert hasattr(siepic, tech["function"])
        assert "SiEPIC" in tech["label"]
        pars = inspect.signature(getattr(siepic, tech["function"])).parameters
        assert len(pars) == len(tech["arguments"])
        for arg in tech["arguments"]:
            assert arg["name"] in pars
            if arg["type"] not in ("medium", "subForm"):
                assert arg["defaults"] == pars[arg["name"]].default


def test_ui_components():
    assert len(_ui_.json["components"]) == len(siepic.component_names)
    assert (
        set(comp["hiddenArguments"]["cell_name"] for comp in _ui_.json["components"])
        == siepic.component_names
    )


def test_json_conversion():
    _ = json.dumps(_ui_.json)
