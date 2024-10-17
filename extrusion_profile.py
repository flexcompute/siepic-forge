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
)

pf.tidy3d_plot(c, y=0)
pyplot.show()
