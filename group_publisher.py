import sys
from collections import namedtuple, defaultdict
import re
from optparse import OptionParser

Publisher = namedtuple('Publisher','prefix year name')

def main(*args):
    with open('publishers') as publishers_file:
        publishers = read_publishers_set(publishers_file)
    publishers_by_name = get_publishers_by_name(publishers)
    output_text(publishers_by_name)
    
        
def get_publishers_by_name(publishers):
    publishers_by_name = defaultdict(set) # Tons of duplictes
    for publisher in publishers:
        sortname = as_sortname(publisher)
        publishers_by_name[sortname].add(publisher)
    return publishers_by_name

SORT_RE = re.compile('\W|\WCo\W|Ltd|Inc|Limited|GbR|GmbH|')
def as_sortname(publisher):
    sortname = publisher.name
    sortname = SORT_RE.sub('', sortname)
    sortname = sortname.lower()
    sortname = sortname.strip()
    return sortname
        
def read_publishers_set(publishers_file):
    publishers = set() # Tons of duplictes
    for i, line in enumerate(publishers_file):
        pub = Publisher(*eval(line))
        publishers.add(pub)
        if i % 10000 == 0:
            print >> sys.stderr, "Processing:", i
            if i == 5000000:
                break
    return publishers

        
def output_rdf(publishers_by_name):
    pass
    
def output_text(publishers_by_name):
    for key in sorted(publishers_by_name):
        pubs = publishers_by_name[key]
        print key, len(pubs)
        for pub in pubs:
            print "\t", pub
            
if __name__ == "__main__":
    sys.exit(main(sys.argv))