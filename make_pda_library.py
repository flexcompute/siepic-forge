import shutil

from tidy3d.config import get_manager

from photonforge import pda

import siepic_forge as siepic
from siepic_forge.component import _component_data

get_manager().switch_profile("dev")


def create_library():
    techs = siepic.ebeam_si(), siepic.ebeam_sin()

    name = "SiEPIC EBeam"
    version = techs[0].version

    for lib in pda.list_libraries(name):
        if lib["version"] == version:
            print("Library already exists: " + str(lib))
            return

    components = [
        siepic.component(n, techs[0 if _component_data[n][0] == "EBeam" else 1])
        for n in siepic.component_names
    ]

    project = pda.create_project(
        name=name,
        description="SiEPIC EBeam Si and SiN PDK",
        visibility="public",
        role="viewer",
        create_template=False,
    )

    # Add sources
    shutil.copytree("./siepic_forge", project.module_path / project.module_name, dirs_exist_ok=True)

    project.save_module()

    # Redirect parametric technology source
    for tech in techs:
        tech.parametric_function = (
            project.module_name + "." + tech.parametric_function.partition(".")[2]
        )

    # Add components
    for component in components:
        print("Adding", repr(component.name), flush=True)
        project.add(component, update_existing_dependencies=False, update_config=False)

    project.add_version(version)

    print("Done:", project)


if __name__ == "__main__":
    pda.init("http://localhost:3030", "ws://localhost:3030")
    try:
        create_library()
    finally:
        pda.stop()
