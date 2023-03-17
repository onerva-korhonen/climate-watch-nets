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

def count_node_and_link_types(G, node_types, node_type_key):
    """
    Calculates the amount of nodes of different types and links between them.

    Parameters:
    -----------
    G: nx.Graph(), a network
    node_types: list of strs, types of nodes for which to calculate the degree distribution
    node_type_key: str, key under which the attribute node type is stored in G.nodes

    Returns:
    --------
    count: dict, number of nodes of different types and links between them
    """
    link_types = []
    for i in range(len(node_types)):
        for j in range(i,len(node_types)):
            link_types.append(node_types[i] + '-' + node_types[j])
    types = node_types + link_types
    count = {t:0 for t in types}
    nodes = G.nodes(data=True)
    links = G.edges()
    for node in nodes:
        node_type = node[1][node_type_key]
        assert node_type in count.keys(), 'Detected unlisted node type {}'.format(node_type)
        count[node_type] += 1
    for link in links:
        start_node_type = nodes[link[0]][node_type_key]
        end_node_type = nodes[link[1]][node_type_key]
        assert start_node_type + '-' + end_node_type in count.keys() or end_node_type + '-' + start_node_type in count.keys(), 'Detected unlisted link type {}'.format(start_node_type + '-' + end_node_type)
        if start_node_type + '-' + end_node_type in count.keys():
            count[start_node_type + '-' + end_node_type] += 1
        else:
            count[end_node_type + '-' + start_node_type] += 1
    return count

def calculate_density_without_linkless_nodes(G):
    """
    Calculates the density of the subgraph induced by nodes that have at least one neighbour.

    Parameters:
    -----------
    G: nx.Graph(), a network

    Returns:
    --------
    density: float
    """
    spanning_nodes = [node for node in G.nodes() if nx.degree(G, node)>0]
    P = G.subgraph(spanning_nodes)
    density = nx.density(P)
    return density

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

def get_log_bins(min_value, max_value, nbins):
    """
    Creates a set of logarithmic bins

    Parameters:
    -----------
    min_value: dbl, minimum value of the data to be binned
    max_value: dbl, maximum value of the data to be binned
    nbins: int, number of bins

    Returns:
    --------
    bins: list of dbl, bin edges
    """
    multiplier = get_log_bins_multiplier(min_value, max_value, nbins)
    bins = [min_value]
    cur_value = bins[0]
    while cur_value < max_value:
        cur_value = cur_value * multiplier
        bins.append(cur_value)
    return bins

def get_log_bins_multiplier(min_value, max_value, nbins):
    """
    Calculates the multiplier for getting a given number of logarithmic
    bins between the given minimum and maximum values.

    Parameters:
    -----------
    min_value: dbl, minimum value of the data to be binned
    max_value: dbl, maximum value of the data to be binned
    nbins: int, number of bins

    Returns:
    --------
    multiplier: dbl, the multiplier for obtaining the logarithmic bins
    """
    assert min_value != 0, '0 given as minimum value for logarithmic bins. Please fix the value.'
    multiplier = np.exp((np.log(max_value/min_value))/nbins)
    return multiplier


