"""
cluster.py
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import pickle
import string
from TwitterAPI import TwitterAPI
from networkx.algorithms.centrality.betweenness import _single_source_shortest_path_basic


def create_graph(followed, followed_total):
    """
    creating nodes and adds edges between people and who they follow
    """
    # TODO
    graph = nx.Graph()
    for i in followed:
        graph.add_node(i)
        for j in range(len(followed[i])):
                graph.add_edge(i,followed[i][j])
    return graph


def draw_network(graph):
    """
    draws network for a given graph
    """
    plt.figure(figsize=(10, 10))
    nx.draw_networkx(graph, with_labels=False,
                      alpha=1.0, width=1.0,
                     node_size=10)
    plt.show()


def girvan_newman(G, most_valuable_edge=None):
    # If the graph is already empty, simply return its connected
    # components.
    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return
    # If no function is provided for computing the most valuable edge,
    # use the edge betweenness centrality.
    if most_valuable_edge is None:
        def most_valuable_edge(G):
            """Returns the edge with the highest betweenness centrality
            in the graph `G`.

            """
            # We have guaranteed that the graph is non-empty, so this
            # dictionary will never be empty.
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    # The copy of G here must include the edge weight data.
    g = G.copy().to_undirected()
    # Self-loops must be removed because their removal has no effect on
    # the connected components of the graph.

    g.remove_edges_from(g.selfloop_edges())
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)

def _without_most_central_edges(G, most_valuable_edge):
    """Returns the connected components of the graph that results from
    repeatedly removing the most "valuable" edge in the graph.

    `G` must be a non-empty graph. This function modifies the graph `G`
    in-place; that is, it removes edges on the graph `G`.

    `most_valuable_edge` is a function that takes the graph `G` as input
    (or a subgraph with one or more edges of `G` removed) and returns an
    edge. That edge will be removed and this process will be repeated
    until the number of connected components in the graph increases.

    """
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        print("edge removed:")
        print(edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components


def main():
    followed = pickle.load( open( 'followed.pkl', 'rb' ) )
    followed_total = pickle.load( open( 'followed_total.pkl', 'rb' ) )
    graph = create_graph(followed, followed_total)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph)
    print("community detection in progress!!!")
    comp = girvan_newman(graph)
    com = tuple(sorted(c) for c in next(comp))
    com = [list(i) for i in com]
    pickle.dump(com, open('comp.pkl', 'wb'))
    for i in com:
        subgraph = graph.subgraph(i)
        nx.draw_networkx(subgraph, with_labels=False,
                         alpha=1.0, width=1.0,
                         node_size=10)
        plt.show()
    print("Clustering completed successfully!!")
    print ("Please run Summarize.py or classify.py if you have not run it before!!")


if __name__ == '__main__':
    main()

#references
#https://networkx.readthedocs.io/en/latest/_modules/networkx/algorithms/community/centrality.html#girvan_newman
