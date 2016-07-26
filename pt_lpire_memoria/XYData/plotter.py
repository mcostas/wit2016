# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 17:22:51 2016

@author: Luis
"""

import pylab

file_title = "tmf_fd"
plots = ["tmf"]
filtered = True
titling = None  # Str or None
mass = 0.52
mean = False
savefile = True
legend = False

if not filtered:
    db = {
        "AR":       ["RF3_52T.txt", "-.", "R"],
        "AR_R":     ["RF3_54T.txt", ":", "R"],
        "AR_Sb":    ["RF3_44T.txt", "--", "R"],
        "AR_RSb":   ["RF3_42T.txt", "-", "R"],
    
        "BR":       ["RF3_55T.txt", "-.", "B"],
        "BR_R":     ["RF3_48T.txt", ":", "B"],
        "BR_Sb":    ["RF3_57T.txt", "--", "B"],
        "BR_RSb":   ["RF3_50T.txt", "-", "B"],
    
        "AFl":      ["RF3_71.txt", "-.", "R"],
        "AFl_R":    ["RF3_69.txt", ":", "R"],
        "AFl_Sb":   ["RF3_70.txt", "--", "R"],
        "AFl_RSb":  ["RF3_65.txt", "-", "R"],
    
        "BFl":      ["RF3_72.txt", "-.", "B"],
        "BFl_R":    ["RF3_73.txt", ":", "B"],
        "BFl_Sb":   ["RF3_74.txt", "--", "B"],
        "BFl_RSb":  ["RF3_76.txt", "-", "B"],

        }
        
else:
    db = {
        "AR":       ["RF3_52T_F.txt", "-.", "R"],
        "AR_R":     ["RF3_54T_F.txt", ":", "R"],
        "AR_Sb":    ["RF3_44T_F.txt", "--", "R"],
        "AR_RSb":   ["RF3_42T_F.txt", "-", "R"],
    
        "BR":       ["RF3_55T_F.txt", "-.", "B"],
        "BR_R":     ["RF3_48T_F.txt", ":", "B"],
        "BR_Sb":    ["RF3_57T_F.txt", "--", "B"],
        "BR_RSb":   ["RF3_50T_F.txt", "-", "B"],
    
        "AFl":      ["RF3_71_F.txt", "-.", "R"],
        "AFl_R":    ["RF3_69_F.txt", ":", "R"],
        "AFl_Sb":   ["RF3_70_F.txt", "--", "R"],
        "AFl_RSb":  ["RF3_65_F.txt", "-", "R"],
    
        "BFl":      ["RF3_72_F.txt", "-.", "B"],
        "BFl_R":    ["RF3_73_F.txt", ":", "B"],
        "BFl_Sb":   ["RF3_74_F.txt", "--", "B"],
        "BFl_RSb":  ["RF3_76_F.txt", "-", "B"],
    
        "RF2_70":   ["RF2_70_stable.txt", "-", "R"],
        "gppb":     ["gppb.txt", "-", "B"],
        "trigmisf": ["trigg_misf.txt", "-", "B"],
        "tmf": ["tmf.txt", "-", "B"],

        }


fig = pylab.figure(figsize=(7,5))

def sea_calc(x,y,speed=10):
    Energyint=0
    for i in range(len(y)-1):
        Energyint = Energyint + (x[i+1]-x[i])*((y[i]+y[i+1])/2)*speed/1000
    return Energyint

prev_y_mean = False
for subplot in plots:
    data = db[subplot][0]; label = subplot
    x = pylab.loadtxt(data)[:,0]*1000
    y = pylab.loadtxt(data)[:,1]
    y_mean = [pylab.mean(y) for i in x]
    y_mean_pos = y_mean[0]
    y_var = [pylab.var(y)]
    y_desv = y_var[0]**.5
    if prev_y_mean:
        if abs(y_mean_pos - prev_y_mean) < 2:
            if y_mean_pos > prev_y_mean:
                y_mean_pos = prev_y_mean + 2
            else:
                y_mean_pos = prev_y_mean - 2
    else:
        prev_y_mean = y_mean_pos
    color=db[subplot][2]
    linestyle=db[subplot][1]
    if mean:
        pylab.plot(x,y_mean, color=color, linestyle='--')
        linestyle='-'
        pylab.text(16.5,float(y_mean_pos),"%.2f ; %.2f" % (y_mean[0], y_desv), color=color)
    pylab.plot(x, y, label=(label+' [%.2f]' % sea_calc(x/mass,y)),
    #pylab.plot(x, y, label=(label),
        color=color, linestyle=linestyle)
    prev_y_mean = y_mean_pos
        
if not mean and legend:
    pylab.legend()
if titling == None:
    pass
else:
    pylab.title(titling)
pylab.xlabel("Time [ms]")
pylab.ylabel("Force [kN]")

if savefile:
    pylab.savefig(file_title+".pdf")

