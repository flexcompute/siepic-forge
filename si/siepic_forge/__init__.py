from .component import component, component_names  # noqa: F401
from .technology import ebeam

__version__ = "1.2.0"


def plot_cross_section(technology=None):
    import photonforge as pf

    if technology is None:
        technology = ebeam()

    c = pf.Component("Extrusion test", technology)
    c.add(
        "Si",
        pf.Rectangle((0, -1), (0.5, 1)),
        "Si Slab",
        pf.Rectangle((-1, -1), (1.5, 1)),
        "Oxide open to BOX",
        pf.Rectangle((-2, -1), (2.5, 1)),
        "Si",
        pf.Rectangle((4.5, -1), (5.5, 1)),
        "M1_heater",
        pf.Rectangle((6, -1), (12, 1)),
        "M2_router",
        pf.Rectangle((8, -1), (12, 1)),
        "M_Open",
        pf.Rectangle((9, -1), (11, 1)),
        "Deep Trench",
        pf.Rectangle((15, -1), (20, 1)),
    )

    ax = pf.tidy3d_plot(c, y=0)
    ax.set(title=technology.name)

    return ax
