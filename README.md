# SiEPIC Forge

This is a technology module for PhotonForge to support [SiEPIC EBeam
PDK](https://github.com/SiEPIC/SiEPIC_EBeam_PDK).

Please note that the 3D structures obtained by extrusion through this
technology are a best approximation of the intended fabricated structures, but
the actuall final dimensions may differ due to several fabrication-specific
effects.


## Usage

The module defines the following functions and attributes:

- Function `ebeam`: generate a `Technology` object supporting SiEPIC EBeam PDK.
- Function `component`: generate pre-defined components from the SiEPIC component library.
- Tuple `component_names`: contains the names of all available components in the library.

Example:

```python
import numpy as np
from matplotlib import pyplot
import photonforge as pf
import siepic_forge as siepic

# Set default technology using default parameters
pf.config.default_technology = siepic.ebeam()

# Get a component from the library
component = siepic.component("ebeam_y_1550")

# Simulate and plot the component's S matrix
pf.plot_s_matrix(pf.C_0 / np.linspace(1.45, 1.62, 171), component=component)
pyplot.show()
```

## Third-Party Licenses

- [`SiEPIC_EBeam_PDK`](https://github.com/SiEPIC/SiEPIC_EBeam_PDK)

  > This project is licensed under the terms of the MIT license.
  > 
  > Copyright (c) 2016-2020, Lukas Chrostowski and contributors
  > 
  > Permission is hereby granted, free of charge, to any person obtaining a
  > copy of this software and associated documentation files (the "Software"),
  > to deal in the Software without restriction, including without limitation
  > the rights to use, copy, modify, merge, publish, distribute, sublicense,
  > and/or sell copies of the Software, and to permit persons to whom the
  > Software is furnished to do so, subject to the following conditions:
  > 
  > The above copyright notice and this permission notice shall be included in
  > all copies or substantial portions of the Software.
  > 
  > THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  > IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  > FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  > AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  > LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  > FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  > DEALINGS IN THE SOFTWARE.
