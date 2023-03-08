# Functions for network analysis

import numpy as np
import networkx as nx

from scipy.stats import binned_statistic

def calculate_degree_distributions(G, node_types, node_type_key, nbins):
    """
    Calculates the degree distributiosn per node type
    
    Parameters:
    -----------
    G: nx.Graph(), a network
    node_types: list of strs, types of nodes for which to calculate the degree distribution
    node_type_key: str, key under which the attribute node type is stored in G.nodes
    nbins: int, number of bins used to calculate the distribution

    Returns:
    --------
    degree_distributions: list of tuples of lists, bin centers and degree distribution of each node type in a separated 
                          tuple of two list
    """
    degree_distributions = []
    for node_type in node_types:
        nodes = get_nodes_per_type(G, node_type, node_type_key)
        if len(nodes) > 0:
            degrees = [G.degree(node) for node in nodes]
            degree_distribution, bin_centers = get_distribution(degrees, nbins)
            degree_distributions.append((bin_centers, degree_distribution))
        else:
            degree_distributions.append(([],[]))
    return degree_distributions

def get_nodes_per_type(G, node_type, node_type_key):
    """
    Finds and returns the nodes of a given type.

    Parameters:
    -----------
    G: nx.Graph(), a network
    node_type: str, the node type to search for
    node_type_key: str, key under which the attribute node type is stored in G.nodes

    Returns:
    --------
    nodes: list, the nodes of the given type
    """
    all_nodes = G.nodes(data=True)
    nodes = []
    for node in all_nodes:
        if node[1][node_type_key] == node_type:
                nodes.append(node[0])
    return nodes

# Accessories

def get_distribution(data, nbins):
    """
    Calculates the PDF of the given data

    Parameters:
    -----------
    data: a container of data points, e.g. list or np.array
    nbins: int, number of bins used to calculate the distribution

    Returns:
    --------
    pdf: np.array, PDF of the data
    bin_centers: np.array, points where pdf has been calculated
    """
    count, bin_edges, _ = binned_statistic(data, data, statistic='count', bins=nbins)
    pdf = count/float(np.sum(count))
    bin_centers = 0.5*(bin_edges[:-1]+bin_edges[1:])

    return pdf, bin_centers
