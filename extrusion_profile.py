#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append("./si")
sys.path.append("./sin")

import siepic_forge as siepic_si
import siepic_sin_forge as siepic_sin
from matplotlib import pyplot

siepic_si.plot_cross_section()

siepic_sin.plot_cross_section()

pyplot.show()
