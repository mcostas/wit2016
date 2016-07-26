# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 20:05:22 2016

@author: Luis
"""

import pylab

E = 200000. #MPa
e1 = 190./E

x = [0, e1, 1]
y = [0, E*e1, 1140]

pylab.plot(x,y, color="black", linestyle='-')
pylab.xlabel("Strain [%]")
pylab.xlim(xmax=0.06)
pylab.ylim(ymax=275.)
pylab.ylabel("Stress [MPa]")
pylab.savefig("steel.pdf")