import photonforge as pf
import siepic_forge as siepic
from matplotlib import pyplot

pf.config.default_technology = siepic.ebeam(
)

c = pf.Component("Extrusion test")
c.add(
    pf.Rectangle((0, -1), (2, 1), layer="Si"),
    
    pf.Rectangle((2.5, -1), (3.5, 1), layer="SiN"),
    
    pf.Rectangle((4, -1), (7, 1), layer="Si slab"),
    pf.Rectangle((5, -1), (6, 1), layer="Si"),
)

model = pf.Tidy3DModel()
sim = model.get_base_simulation(c, pf.C_0 / 1.55)
sim.plot_structures(y=0)

pyplot.show()
