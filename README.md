* Publisher Grouping

Group publisher tuples by publisher name

** Usage

	Usage: group_publisher.py [options] publisher_tuples

	Options:
	  -h, --help            show this help message and exit
	  -f FORMAT, --format=FORMAT
	  -n SAMPLE_SIZE, --sample-size=SAMPLE_SIZE

Example Usage:

	python group_publisher.py --format rdf publishers > publishers.rdf

** Requirements

Requires latest `pymantic` for RDF output. 

	pip install https://github.com/oreillymedia/pymantic/tarball/master

Text output has no requirements out side of the standard library.
