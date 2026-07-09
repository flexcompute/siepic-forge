import shutil

import photonforge as pf
from photonforge import pda

import siepic_sin_forge as siepic


def ignore_components(path, names):
    return [n for n in names if n == "library" or "component" in n]


def create_library():
    name = "SiEPIC EBeam SiN"
    description = "SiEPIC EBeam SiN PDK"
    version = siepic.ebeam().version

    for lib in pda.list_libraries(name):
        if lib["version"] == version:
            print(f"Library already exists: {lib!r}")
            return

    print(f"Creating library {name!r} - version {version!r}", flush=True)
    project = pda.create_project(
        name=name,
        description=description,
        visibility="public",
        role="viewer",
        create_template=False,
    )

    # Add sources: static components will be added directly, so we don't need the reference GDS
    shutil.copytree(
        "./siepic_sin_forge",
        project.module_path / project.module_name,
        dirs_exist_ok=True,
        ignore=ignore_components,
    )

    # Patch __init__ to remove components
    init = project.module_path / project.module_name / "__init__.py"
    init.write_text(
        "\n".join(x for x in init.read_text().splitlines() if not x.startswith("from .component"))
        + "\n"
    )

    project.save_module()
    module = project.import_module(None)[project.module_name]

    tech = module.ebeam()
    pf.config.default_technology = tech

    components = [siepic.component(n, tech) for n in siepic.component_names]

    # Add components
    update_config = True
    for component in components:
        print("Adding", repr(component.name), flush=True)
        project.add(component, update_existing_dependencies=False, update_config=update_config)
        update_config = False

    project.add_version(version)

    print(f"Done: {project!r}")


if __name__ == "__main__":
    pda.init()

    try:
        create_library()
    finally:
        pda.stop()
