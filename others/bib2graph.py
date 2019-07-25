import sys
import bibtexparser
import networkx as nx
import pydot
from collections import Counter
import graphviz
from graphviz import Digraph
import matplotlib.pyplot as plt

from subprocess import call

TAG_MAP = {
    't': 'toread',
    'm': 'mapped',
    'i': 'inprogress',
    'r': 'read'}


def unpack(citationString):
    return [s.strip() for s in citationString.split(',')]


def quick_stats(bibtex):
    stats = Counter()
    for key, entry in bibtex.entries_dict.items():
        tag = entry.get('tags')
        if tag:
            newtag = ''
            for t in tag:
                newtag += TAG_MAP[t] + ' '
            tag = newtag
        stats[tag] += 1
    return stats


# The following are the node classes
#   r, i, t - read, in progress, to read
#   m - maps/includes all (relevant) work citing this node at the time of writing

def main():
    bibfile = sys.argv[1]
    parsere = bibtexparser.bparser.BibTexParser(common_strings=True)

    with open(bibfile) as bibtex_file:
        bibtex = bibtexparser.load(bibtex_file, parser=parsere)

    stats = quick_stats(bibtex)
    for k, v in stats.items():
        print("{0:>5} --> {1:}".format(v, k))

    citations = {}
    tags = {}

    print(len(bibtex.entries_dict))
    for key, entry in bibtex.entries_dict.items():
        cites = entry.get('cites')
        if cites:
            citations[key] = unpack(cites)
        t = entry.get('tags')
        if t:
            tags[key] = t

    G = nx.DiGraph()
    for key, entry in citations.items():
        for cit in entry:
            G.add_edge(key, cit)

    # nx.draw(G)
    # plt.show()

    pydot_G = nx.nx_pydot.to_pydot(G)
    for node in pydot_G.get_nodes():
        t = node.get_name()
        if t and tags.get(t):
            node.set('nodetype', tags.get(t))

    pydot_G.set('rankdir', 'LR')
    pydot_G.set('style', 'dashed')
    pydot_G.write('bib.dot')

    # u = Digraph(name='bib', filename='bib.gv')
    # u.view()

    call(["gvpr -c -f filter.gvpr bib.dot > bib_nice.dot"], shell=True)
    call(["ccomps -x bib_nice.dot | dot | gvpack -array1 | circo -Tpng -n2 -o bib.png"], shell=True)


if __name__ == '__main__':
    main()
