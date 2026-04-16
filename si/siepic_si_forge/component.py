import warnings

try:
    from importlib.resources import as_file, files
except ImportError:
    from importlib_resources import as_file, files

import photonforge as pf
import photonforge.typing as pft

from ._component_data import _component_data

component_names = set(_component_data.keys())


def component(
    cell_name: str,
    technology: pf.Technology | None = None,
    tidy3d_model_kwargs: pft.kwargs_for(pf.Tidy3DModel) = {},
) -> pf.Component:
    """Load a component from the default PDK library.

    Args:
        cell_name (str): Name of the component to load.
        technology (Technology): Technology for the created component.
        tidy3d_model_kwargs (dict): Keyword arguments passed to the Tidy3D
          model of the created component.

    Returns:
        Component: Component loaded from the default PDK library.

    Note:
        The available component names are listed in the module-level tuple
        ``component_names``.
    """
    libname, port_data, kwargs, thumbnail = _component_data.get(
        cell_name, (None, None, None, None)
    )

    if technology is None:
        technology = pf.config.default_technology
        if "SiEPIC" not in technology.name:
            warnings.warn(
                f"Current default technology {technology.name} does not seem compatible with the "
                f"SiEPIC component library",
                RuntimeWarning,
                2,
            )

    # Load library cell
    gdsii = files("siepic_si_forge") / "library" / (libname + ".gds")
    with as_file(gdsii) as fname:
        c = pf.load_layout(fname, technology=technology)[cell_name]

    if thumbnail:
        c.properties.__thumbnail__ = thumbnail

    for layer, labels in c.labels.items():
        for label in labels:
            if "lumerical" in label.text.lower():
                c.remove(label, layer=layer)

    # Add ports
    z = (
        0.1
        + technology.parametric_kwargs.get("top_oxide_thickness", 3.0)
        + technology.parametric_kwargs.get("passivation_oxide_thickness", 0.3)
    )
    port_error = False
    for data in port_data:
        if len(data) == 3:
            if isinstance(data[1], tuple):
                terminal = pf.Terminal(
                    technology.layers[data[2]].layer, pf.Rectangle(center=data[0], size=data[1])
                )
                c.add_terminal(terminal)
            else:
                port_spec = technology.ports.get(data[2])
                if port_spec is None:
                    port_error = True
                    warnings.warn(
                        f"Required port spec {data[2]} not available in technology "
                        f"{technology.name!r}. Port skipped.",
                        RuntimeWarning,
                        2,
                    )
                else:
                    port = pf.Port(data[0], data[1], port_spec)
                    c.add_port(port)
        else:
            port = pf.GaussianPort(
                data[0] + (z,),
                data[1],
                waist_radius=data[2],
                polarization_angle=data[3],
            )
            c.add_port(port)

    # Add model
    if kwargs is not None:
        kwargs = dict(kwargs)
        if port_error and "port_symmetries" in kwargs:
            del kwargs["port_symmetries"]
        kwargs.update(tidy3d_model_kwargs)
        c.add_model(pf.Tidy3DModel(**kwargs), "Tidy3D")

    return c
