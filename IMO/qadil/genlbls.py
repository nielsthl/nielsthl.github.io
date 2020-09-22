# -*- coding: utf-8 -*

import sys
import glob
import re
import csv
import io
#import os

from os.path import basename, splitext

chapterdir = sys.argv[1]

lblsfiles = glob.glob(chapterdir+'/*.lbl')
htmlfiles = glob.glob(chapterdir+'/*.html')

chapterlist=[]
dict={}
sectioncount = 1

#
# Label files format:
#
# label, htmllabelnamewithindex ("env", "equ", "sec" as prefix)
#
# Examples:
#
# eqstart, equ2.1
# poldivthm, env2.14
# subsecfirst, sec1.5.1
#


for f in lblsfiles:
    with open(f, "r") as fil:
        #htmlfilename = os.path.basename(f).split(".")[0]+".html"
        htmlfilename = splitext(basename(f))[0]+".html"
        csvreader = csv.reader(fil)
        for li in csvreader:
            dict[li[0]] = [htmlfilename, li[1].lstrip()] 

def labeltype(str):
    #
    # "equ2.1" -> "equ"
    #
    if str[:3] in ["equ", "env", "sec"]:
        return str[:3]
    else:
        return str

def index(str):
    #
    # "equ2.1" -> "2.1"
    #
    if str[:3] in ["equ", "env", "sec"]:
        return str[3:]
    else:
        return str

    return str[3:]
            
def lookuplabel(matchobj):
    label = matchobj.group(1)
    try:
        repl = dict[label]
        fname = repl[0]
        htmllabel = repl[1]
        ltyp = labeltype(htmllabel)
        ind = index(htmllabel)
    except:
        return "UNDEFINED: " + label
    if ltyp == "equ":
        return f'<a href="{fname}#{htmllabel}">({ind})</a>'
    else:
        return f'<a href="{fname}#{htmllabel}">{ind}</a>'

def mathmodelookuplabel(matchobj):
    label = matchobj.group(1)
    try:
        repl = dict[label]
        fname = repl[0]
        htmllabel = repl[1]
        ind = index(htmllabel)
    except:
        return "UNDEFINED: " + label
    return f'\\href{{{fname}#{htmllabel}}}{{{ind}}}'

regex = '\{\?\}(.*?)\{\/\?\}' # {?}niels{/?}
regc = re.compile(regex)

regexmath = '\{\*\}(.*?)\{\/\*\}' # {*}niels{/*}
regcmath = re.compile(regexmath)

for f in htmlfiles:

    with open(f, "r") as fil:
        str = fil.read()
        
    str = regc.sub(lookuplabel, str)
    str = regcmath.sub(mathmodelookuplabel, str)
    
    with open(f, "w") as fil:
        fil.write(str)


    


