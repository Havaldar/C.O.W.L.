import networkx as nx
import numpy as np
import scipy as sp
from numpy import linalg as la
import math
import sys

def load_vertices(graph, file):
    with open(file, 'rU') as data:
        reader = data.read().split('\n')
        for row in reader[1:]:
            vertice = row.replace('"','').split()
            if int(vertice[0])<=6486: graph.add_node(vertice[0],name=''.join(vertice[1:]).replace("'",'').replace('"',''),type='hero')

def load_edges(graph, file):
    comics = {}
    with open(file, 'rU') as data:
        reader = data.read().split('\n')
        for row in reader[1:]:
            row_arr = row.split()
            for comic in row_arr[1:]:
                character = row_arr[0]
                try: comics[comic].append(character)
                except KeyError: comics[comic] = [character]
    for comic in comics:
        chars = comics[comic]
        num_chars = len(chars)
        edges = [[(comics[comic][v],comics[comic][w]) for w in xrange(v+1,len(comics[comic]))] for v in xrange(len(comics[comic]))]
        graph.add_edges_from([edge for sublist in edges for edge in sublist])

def get_fiedler_vector(laplacian):
    eig_vals, eig_vectors = la.eig(laplacian)
    seen = {}
    uniq_eig = []
    for (val, vector) in zip(eig_vals, eig_vectors):
        if val in seen: continue
        else:
            seen[val] = True
            uniq_eig.append((val, vector))
    try: return sorted(uniq_eig)[1][1]
    except IndexError: return uniq_eig[0][1]

def min_cut(graph):
    lap = nx.laplacian_matrix(graph).toarray()
    fiedler_vector = get_fiedler_vector(lap)
    result_vector = lap.dot(fiedler_vector)
    nodes = graph.nodes()
    partition_one = set()
    partition_two = set()
    median = sorted(result_vector)[len(result_vector) / 2]

    for i in xrange(len(result_vector)):
        if result_vector[i] == median:
            p = partition_one if len(partition_one) < len(partition_two) else partition_two
            p.add(nodes[i])
        elif result_vector[i] < median:
            partition_one.add(nodes[i])
        else:
            partition_two.add(nodes[i])

    return (partition_one, partition_two)

def find_closest_chars(graph, node, k):
    print len(graph.nodes())
    partition_a, partition_b = min_cut(graph)
    print partition_a, partition_b
    if k < len(partition_a) and k < len(partition_b):
        return find_closest_chars(graph.subgraph(partition_a if node in partition_a else
                                      partition_b), node, k)
    else:
        return graph.subgraph(partition_a if node in partition_a else partition_b)

def draw_graph(graph, character):
    nodes = graph.nodes()
    centrality = nx.eigenvector_centrality_numpy(g)
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 12))
    graph.node[character]["type"] = "center"
    valmap = { "hero":  0.54, "center": 0.87 }
    types = nx.get_node_attributes(graph, "type")
    values = [valmap.get(types[node], 0.25) for node in nodes]
    sizes = [int(centrality[node] * 400) for node in nodes]
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_nodes(graph, pos, node_size=sizes, node_color=values, cmap=plt.cm.hot, with_labels=False)
    plt.show()

def main():
    name = sys.argv[1]
    num = int(sys.argv[2])
    graph = nx.Graph(name="C.O.W.L.")
    load_vertices(graph, 'vertices.txt')
    load_edges(graph, 'edges.txt')
    partition = find_closest_chars(graph, name, num)
    draw_graph(partition)

if __name__ == 'main':
    main()
