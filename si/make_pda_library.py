import shutil
from argparse import ArgumentParser

import photonforge as pf
from photonforge import pda
from tidy3d.config import get_manager

import siepic_forge as siepic

get_manager().switch_profile("dev")


def create_library():
    tech = siepic.ebeam()
    pf.config.default_technology = tech

    name = "SiEPIC EBeam"
    version = tech.version

    for lib in pda.list_libraries(name):
        if lib["version"] == version:
            print("Library already exists: " + str(lib))
            return

    components = [siepic.component(n) for n in siepic.component_names]

    project = pda.create_project(
        name=name,
        description="SiEPIC EBeam Si PDK",
        visibility="public",
        role="viewer",
        create_template=False,
    )

    # Add sources
    shutil.copytree("./siepic_forge", project.module_path / project.module_name, dirs_exist_ok=True)

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
    parser = ArgumentParser(prog=__file__)
    parser.add_argument("--profile", default=None, help="tidy3d configuration profile")
    args = parser.parse_args()

    profile = args.profile
    if args.profile is not None:
        get_manager().switch_profile(args.profile)

    pda.init()

    try:
        create_library()
    finally:
        pda.stop()
