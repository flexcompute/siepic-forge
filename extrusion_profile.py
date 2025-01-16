import photonforge as pf
import siepic_forge as siepic
from matplotlib import pyplot

pf.config.default_technology = siepic.ebeam()

c = pf.Component("Extrusion test")
c.add(
    "Si",
    pf.Rectangle((0, -1), (2, 1)),
    "SiN",
    pf.Rectangle((2.5, -1), (3.5, 1)),
    "Si slab",
    pf.Rectangle((4, -1), (7, 1)),
    "Si",
    pf.Rectangle((5, -1), (6, 1)),
    "M1_heater",
    pf.Rectangle((-0.5, -1), (2.5, 1)),
    "M2_router",
    pf.Rectangle((4, -1), (6, 1)),
    "M_Open",
    pf.Rectangle((4.5, -1), (5.5, 1)),
    "Si",
    pf.Rectangle((-3, -1), (-1, 1)),
    "Oxide open (to BOX)",
    pf.Rectangle((-2.5, -1), (-1.5, 1)),
    "Deep Trench",
    pf.Rectangle((-5, -1), (-4, 1)),
)

pf.tidy3d_plot(c, y=0)
pyplot.show()
