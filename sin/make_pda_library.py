import shutil

import photonforge as pf
from photonforge import pda
from tidy3d.config import get_manager

import siepic_sin_forge as siepic

get_manager().switch_profile("dev")


def create_library():
    tech = siepic.ebeam()
    pf.config.default_technology = tech

    name = "SiEPIC EBeam SiN"
    version = tech.version

    for lib in pda.list_libraries(name):
        if lib["version"] == version:
            print("Library already exists: " + str(lib))
            return

    components = [siepic.component(n) for n in siepic.component_names]

    project = pda.create_project(
        name=name,
        description="SiEPIC EBeam SiN PDK",
        visibility="public",
        role="viewer",
        create_template=False,
    )

    # Add sources
    shutil.copytree(
        "./siepic_sin_forge", project.module_path / project.module_name, dirs_exist_ok=True
    )

    project.save_module()

    # Redirect parametric technology source
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
