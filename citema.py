import numpy as np
import urllib2
import xml.etree.ElementTree as ET
import os
import json

# Main method
def makeMap(inipmid,levels=2):

    output = map2json(buildMap(inipmid,levels),filename=str(inipmid)+'.json')
    
    # output json file
    filename = str(inipmid)+'.json'
    s = open(filename, 'w')
    s.write(json.dumps(output, indent=4, separators=(',', ': ')))
    s.close()
    
    return None

# Output JSON from buildmap output
def map2json(ids,filename='map.json'):
    output = {}
    
    # build nodes
    output['nodes'] = []
    key2ind = []
    for key in ids.keys():
        output['nodes'].append({'name':str(key),'group':(ids[key]['level']+1)})
        key2ind.append(key)

    # build links        
    output['links'] = []
    for key in ids.keys():
        for target in ids[key]['IDs']:
            output['links'].append({'source': key2ind.index(key),'target': key2ind.index(target),'value':1})

    return output

# Returns dictionary of PMID keys and PMIDs values
def buildMap(inipmid,levels=3,ids={}):
    curIDs = getIDs(inipmid)
    if inipmid not in ids:
        ids[inipmid] = {'IDs':curIDs,'level':levels}

    if levels > 1:
        for curID in curIDs:
            if curID not in ids:
                ids = buildMap(curID,levels-1,ids)
    else:
        for curID in curIDs:
            if curID not in ids:
                ids[curID] = {'IDs':[],'level':levels-1}

    return ids
# Returns pmids from citation pmid, if any.
# If none exist, returns None
def getIDs(pmid):

    # get local xml from pubmed
    filename = url2xml(pmid)

    # find the PMID field
    xmlroot = ET.parse(filename).getroot()
    PMIDs = []
    for curid in xmlroot.getiterator('PMID'):
        PMIDs.append(int(curid.text))
    killfile(filename)

    return PMIDs

# Returns URL for pmid pubmed xml file
def getURL(pmid):
    return 'http://www.ncbi.nlm.nih.gov/pubmed/'+str(pmid)+'?report=xml'

# Makes a local XML file from a URL you to play with,
# and returns the filename, directory
def url2xml(pmid):
    filehandle = urllib2.urlopen(getURL(pmid))
    filecontent = urllib2.unquote(filehandle.read())
    filecontent = filecontent.replace("&lt;", "<")
    filecontent = filecontent.replace("&gt;", ">")
    filename = str(pmid)+'.xml'
    s = open(filename, 'w')
    s.write(filecontent)
    s.close()
    
    return filename
    

def killfile(filename):
    os.remove(filename)
    return None
