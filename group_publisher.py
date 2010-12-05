import sys
from collections import namedtuple, defaultdict
import re
from optparse import OptionParser

Publisher = namedtuple('Publisher','prefix year name')

def main():
    usage = "usage: %prog [options] publisher_tuples"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--format", action="store", type="choice", 
                      choices=["rdf", "text"], default="text", dest="format")
    parser.add_option("-n", "--sample-size", action="store", type=int, 
                      default=None, dest="sample_size")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Must specify publisher_tuples file")
    publishers_file_name = args[0]
    with open(publishers_file_name) as publishers_file:
        publishers = read_publishers_set(publishers_file, 
                                         options.sample_size)
    publishers_by_name = get_publishers_by_name(publishers)
    if options.format == 'rdf':
        output_rdf(publishers_by_name)
    elif options.format == 'text':
        output_text(publishers_by_name)
    
        
def get_publishers_by_name(publishers):
    """Return publishers in a dict indexed by sortname"""
    publishers_by_name = defaultdict(set) # Tons of duplictes
    for publisher in publishers:
        sortname = as_sortname(publisher)
        publishers_by_name[sortname].add(publisher)
    return publishers_by_name

ignore_words = ["publishing", "co", "pub", "inc", "ltd", "company"]
NON_CHAR = re.compile(r'\W')
def as_sortname(publisher):
    """Convert the publisher name in to it's sortable key for grouping."""
    sortname = publisher.name
    sortname = sortname.lower()
    tokens = NON_CHAR.split(sortname)
    sortname = "".join(token for token in tokens if token not in ignore_words)
    sortname = sortname.lower()
    return sortname
        
def read_publishers_set(publishers_file, sample_size=None):
    """Return a set from a file containing python tuples in the form:
    (u'0220', 1996, u'Penguin')
    (u'0669', 1990, u'D.C. Heath & Co')
    Stop after reading sample_size number of tuples to nearest 10,000
    """
    publishers = set()
    for i, line in enumerate(publishers_file):
        pub = Publisher(*eval(line))
        publishers.add(pub)
        if i % 10000 == 0:
            print >> sys.stderr, "Processing:", i
            if sample_size and i >= sample_size:
                break
    print >> sys.stderr, "Processed:", i , "Unique Publishers:", len(publishers)
    return publishers

        
def output_rdf(publishers_by_name):
    """Output RDF N3 for each publisher in the form:
    pub:oreillymedia a foaf:Organization;
    foaf:name "O' Reilly Media Inc."@en,
        "O'Reilly Media"@en,
        "O'Reilly Media Inc"@en,
        "O'Reilly Media Inc."@en,
        "O'Reilly Media, Inc."@en,
        "O'ReillyMedia, Inc."@en,
        "O'reilly Media"@en .
    """
    import pymantic.RDF
    import rdflib
    graph = rdflib.ConjunctiveGraph()
    @pymantic.RDF.register_class('foaf:Organization')
    class Organization(pymantic.RDF.Resource):
        namespaces = {'foaf':'http://xmlns.com/foaf/0.1/'}        
    for key in publishers_by_name:
        uri = "http://gavin.carothers.name/work/archive/publishers/%s" % key
        publisher = Organization.new(graph, uri)
        pubs = publishers_by_name[key]
        names = set()
        for pub in pubs:
            names.add(pub.name)
        publisher['foaf:name'] = names
    graph.bind('pub', rdflib.Namespace('http://gavin.carothers.name/work/archive/publishers/'))
    graph.bind('foaf', rdflib.Namespace('http://xmlns.com/foaf/0.1/'))
    print graph.serialize(format='n3')
    
def output_text(publishers_by_name):
    """Output plain text with Publisher tuples in the form:
    mcgrawhill 3
        Publisher(prefix=u'007', year=1989, name=u'McGraw-Hill')
        Publisher(prefix=u'000', year=1991, name=u'McGraw Hill')
        Publisher(prefix=u'000', year=1986, name=u'McGraw Hill')
    """
    for key in sorted(publishers_by_name):
        pubs = publishers_by_name[key]
        print key, len(pubs)
        for pub in pubs:
            print "\t", pub
            
if __name__ == "__main__":
    sys.exit(main())