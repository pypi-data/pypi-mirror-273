import lxml

from lxml import etree

def loadStaxml(filename):
    with open(filename, "r") as inxml:
        return etree.parse(inxml)

def findStation(staxml, net, sta):
    for n in staxml

def findChannel(staxml, net, sta, loc, chan):
    pass

def main():
