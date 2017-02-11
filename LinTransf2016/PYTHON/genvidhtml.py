#!/usr/bin/python
# -*- coding: utf-8 -*

#
# Great coding, Friday 1/22/2016:
#
# XML is not the right format for video annotation.
#
# DIY: Python's regex module is very powerful!
#
# Extended, Wednesday 1/27/2016: Parameters.
#
# Usage:
# Carried out in EDTECH directory
#
# python genvidhtml.py <anvfil = test.anv> <blankskabelon=blank.html>
#
# Output is then test.html.
#

import re
import sys 
import io 
import string

ANVroot = "ANV/"

#
# Simple regexes for parsing the almost xml file containing events
#

pvideo = re.compile('<video>(.*?)</video>')
ptitle = re.compile('<title>(.*?)</title>')
pintro = re.compile('<intro>(.*?)</intro>')
pposter = re.compile('<poster>(.*?)</poster>')


pevent = re.compile('<event:(.*?)>(.*?)</event>')
premark = re.compile('<remark>(.*?)</remark>')
premarkpause = re.compile('<remarkpause>(.*?)</remarkpause>')
pquiz = re.compile('<quiz>(.*?)</quiz>')
pquestion = re.compile('<question>(.*?)</question>')
panswer = re.compile('<answer:(.*?)>(.*?)</answer>')

#
#
#

#
# Handling input files
#
# Notice directory assumptions: ANV--test.anv produces test.html in EDTECH directory
#
#

filstr = sys.argv[1]
filind = io.open(ANVroot + filstr, "r", encoding="utf8")

#
# Notice "test.anv" maps to the output file name "test.html":
#


filudstr = string.split(filstr, ".")[0] + ".html"
filud = io.open(filudstr, "w", encoding="utf8")
 
skabelonfil = io.open(sys.argv[2], encoding="utf8")
skabelon = skabelonfil.read()
#skabelon = skabelon.replace('\n', ' ')


#print skabelon

datastr = filind.read().replace('\n', ' ')
filind.close()
skabelonfil.close()

#datastr = re.sub('\\\\', '\\\\\\\\', datastr) # SUK :-)
datastr = re.sub(' +', ' ', datastr)
#datastr = re.sub('> +', '>', datastr)
#datastr = re.sub(' +<', '<', datastr)

videostr = pvideo.findall(datastr)[0]
titlestr = ptitle.findall(datastr)[0]
introstr = pintro.findall(datastr)[0]
posterstr = pposter.findall(datastr)[0]


foundevents = pevent.findall(datastr)

timesstr = "var eventtimes = ["
eventsstr = "var events = ["

#
# Take introstr into account as a remark event if user rewinds (in anv file! SUK!!)
#


for ev in foundevents:
    timesstr += ev[0] + ","
    estr = ev[1]
    foundremark = premark.findall(estr)
    if (foundremark != []):
        eventsstr += '[\'remark\', \''+ foundremark[0]+ '\'],'
        continue
    foundremarkpause = premarkpause.findall(estr)
    if (foundremarkpause != []):
        eventsstr += '[\'remarkpause\', \''+ foundremarkpause[0]+ '\'],'
        continue
    
    foundquiz = pquiz.findall(estr)
    spsm = pquestion.findall(foundquiz[0])[0]
    txt = '<h2 style=\"color:red;\">Quiz</h2>'+spsm+'<br><br>'
    
    svar = panswer.findall(foundquiz[0])
    anscolors = '['

    for ix, a in enumerate(svar):
        if(a[0] == "true"): 
            anscolors += '\"green\",'
        else:
            anscolors += '\"red\",'
        txt += '<div id=ans'+str(ix)+'><label for="yo'+str(ix)+'"><input id="yo'+str(ix)+'" type=\"checkbox\" value=\"\"/>  '+ a[1] + '</div><br>'
        
    anscolors = anscolors[:-1] + ']'
    eventsstr += '[\"quiz\", \''+ txt + '\', ' + anscolors + '],'
      
eventsstr = eventsstr[:-1] + ']'
timesstr = timesstr[:-1] + ']'

bigstr = eventsstr + ";" + timesstr + ";"

replstr = skabelon.replace("{0}", videostr)
replstr = replstr.replace("{1}", titlestr)
replstr = replstr.replace("{3}", introstr)
replstr = replstr.replace("{2}", posterstr)
replstr = replstr.replace("{4}", bigstr)

print "OUTPUT written on " + filudstr

filud.write(replstr)
filud.close()

