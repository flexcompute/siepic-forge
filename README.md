# SiEPIC Forge

This python module implements the [SiEPIC EBeam
PDK](https://github.com/SiEPIC/SiEPIC_EBeam_PDK) PDK as components and
technology specification for
[PhotonForge](https://docs.flexcompute.com/projects/photonforge/)


## Installation

### Python interface

Installation via `pip`:

    pip install siepic-forge


### PhotonForge Web UI

1. [Download from PyPI](https://pypi.org/project/siepic-forge/#files) the
   latest wheel file: `imec_isipp200_ip_forge-*-py3-none-any.whl`.

2. In the PhotonForge web interface, upload that file to load the EBeam PDK.


## Usage

The simplest way to use the this PDK in PhotonForge is to set its technology as
default:

    import photonforge as pf
    import siepic_forge as siepic

    tech = siepic.ebeam()
    pf.config.default_technology = tech


The `ebeam` function creates a parametric technology and accepts a number of
parameters to fine-tune the technology.

PDK components are available through the `component` function, which takes a
component name as first argument. The list of component names is available as a
set `component_names`:

    print(siepic.component_names)
    
    pdk_component = siepic.component("ebeam_y_1550")


More information can be obtained in the documentation for each function:

    help(siepic.ebeam)

    help(siepic.component)


## Warnings

Please note that the 3D structures obtained by extrusion through this module's
technologies are a best approximation of the intended fabricated structures,
but the actual final dimensions may differ due to several fabrication-specific
effects. In particular, doping profiles are represented with hard-boundary,
homogeneous solids, but, in practice will present process-dependent variations
with smooth boundaries.


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
