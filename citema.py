import numpy as np
import urllib2
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom


# Returns pmids from citation pmid, if any.
# If none exist, returns None
def getIDs(pmid):

    # get local xml from pubmed
    filename = url2xml(pmid)

    # find the PMID field
    xmlroot = ET.parse(filename).getroot()
    PMIDs = []
    for curid in xmlroot.iter('PMID'):
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
