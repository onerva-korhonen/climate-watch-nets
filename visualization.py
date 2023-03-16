# functions for visualization

import matplotlib.pylab as plt
import networkx as nx
import numpy as np

from collections import Counter
from networkx.drawing.nx_agraph import graphviz_layout

import importlib.util

spec = importlib.util.spec_from_file_location('network_analysis','/home/onerva/projects/climate_watch/climate-watch-nets/network_analysis.py')
network_analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network_analysis)


def draw_network(G, node_type_key='node_type', layout='graphviz', node_colors={}, node_markers={}, node_size=50, edge_width=1, edge_alpha=0.5, arrow_size=5, save_path_base='', save_name=''):
    """
    Visualizes the network and saves the plot as pdf. If save path is not given, the figure is shown instead of saving.

    Parameters:
    -----------
    G: networkx.graph(), the network to be visualized
    node_type_key: str, key under which the attribute node type is stored in G.nodes
    layout: str, layout to be used for visualizing the network (options: 'graphviz', 'spring')
    node_colors: dict, color of each node type (keys: node types)
    node_markers: dict, marker of each node type (keys: node types)
    node_size: scalar, node size in the visualization
    edge_widht: dbl or str, width of network edges, set to 'weight' to use individual edge weights
    edge_alpha: dbl, opacity of edges
    arrow_size: int, size of the arrowheads in the visualization
    save_path_base: str, a base path (e.g. to a shared folder) for saving figures
    save_name: str, name of the file where to save the network visualization

    Returns:
    --------
    No direct output, saves the network visualization as pdf
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    assert layout in ['graphviz','spring'],"Check graph layout, options: 'graphviz','spring'"
    if layout == 'graphviz':
        pos = graphviz_layout(G, prog='dot')
    elif layout == 'spring':
        pos = nx.spring_layout(G)
    nodes = G.nodes(data=True)
    # reading node types
    assert Counter(node_colors.keys()) == Counter(node_markers.keys()), "Node color and marker keys don't match, check the keys!"
    node_types = set(node_colors.keys())
    
    # drawing nodes of each type separately
    for node_type in node_types:
        nodes_to_add = network_analysis.get_nodes_per_type(G, node_type, node_type_key)
        #for node in nodes:
        #    if node[1][node_type_key] == node_type:
        #        nodes_to_add.append(node[0])
        nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=nodes_to_add, node_color=node_colors[node_type], node_shape=node_markers[node_type], node_size=node_size,label=node_type)
    
    # drawing edges
    if edge_width == 'weight':
        edges = list(G.edges())
        weights = [G[edge[0]][edge[1]]['weight'] for edge in edges]
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, width=weights, alpha=edge_alpha)
    else:
        edges = list(G.edges())
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, width=edge_width, alpha=edge_alpha, arrowsize=arrow_size)

    # saving network
    if save_path_base:
        assert len(save_name)>0, 'Give a file name for saving the visualization!'
        save_path = save_path_base + '/' + save_name
        plt.savefig(save_path, format='pdf', bbox_inches='tight')
        plt.close()
    else:
        plt.show()
        plt.close()

def plot_curves(data, normalize=False, x_label='', y_label='', labels=[], colors='b', markers='', line_style='-', line_width=1.5, alpha=0.5, save_path=''):
    """
    Plots the given distributions and saves them into a .pdf file

    Parameters:
    -----------
    data: list of tuples of lists, each tuple containing the lists of x and y values to plot
    normalize: if true, x values are normalized by their maximum before plotting.
    x_label: str, label of the x axis
    y_label: str, label of the y axis
    labels: list, labels for each curve to be plotted
    colors: str or list, color for each curve to be plotted
    markers: str or list, data point markers of each curve to be plotted
    line_style: str, line style of the curves
    line_width: float, line widht of the curves
    alpha: float, transparency of the visualization
    save_path: str, path to which to save the figure

    Returns:
    --------
    No direct output, saves the curves in a pdf file
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if not isinstance(colors, list):
        colors = [colors for i in range(len(data))]
    if not isinstance(markers, list):
        markers = [markers for i in range(len(data))]

    assert len(colors) == len(data), "Length of colors list don't match length of data, please check or give a scalar value"
    assert len(markers) == len(data), "Length of markers list don't match length of data, please check or give a scalar value"

    if len(labels) > 0:
        if not isinstance(labels, list):
            labels = [labels for i in range(len(data))]
        assert len(labels) == len(data), "Length of labels list don't match length of data, please check"
        for (x, y), label, color, marker in zip(data, labels, colors, markers):
            if normalize:
                x = x/max(x)
            plt.plot(x, y, label=label, color=color, marker=marker, linestyle=line_style, linewidth=line_width, alpha=alpha)
            plt.legend()
    else:
        for (x, y), color, marker in zip(data, colors, markers):
            if normalize:
                x = x/max(x)
            plt.plot(x, y, color=color, marker=marker, linestyle=line_style, linewidth=line_width, alpha=alpha)

    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    if save_path:
        plt.savefig(save_path, format='pdf', bbox_inches='tight')
        plt.close()
    else:
        plt.show()
        plt.close()

def visualize_node_and_link_type_count(counts, bin_type='logarithmic', nbins=10, color='b',bar_width=0.75, save_path_base='', save_name=''):
    """
    Visualizes the count of node and link types as a histogram and saves
    the visualization as pdf. Node and link types that don't appear in the data
    (i.e. for which counts[type] = [0 .. 0]) are omitted from visualization.

    Parameters:
    -----------
    counts: dict, count of node and link types
    bin_type: str, 'linear' or 'logarithmic'
    nbins: int, number of bins
    color: str, color of the histogram bars
    bar_width: dbl, widht of the histogram bars
    save_path_base: str, path to which save the visualization
    save_name: str, base name for the file to which to save the visualization, this base will
                    be combined with each node and link type to form the actual
                    file name

    Returns:
    --------
    no direct output, saves the visualization in a pdf file
    """
    assert bin_type in ['linear', 'logarithmic'], "Unknown bin type, please give 'linear' or 'logarithmic'" 
    assert len(save_name) > 0, 'Please give file name for saving the node and link type histograms'
    for key in counts:
        data = counts[key]
        if np.max(data) > 0:
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if bin_type == 'linear':
                bins = np.linspace(np.min(data), np.max(data), nbins)
            elif bin_type == 'logarithmic':
                min_value = np.min(data)
                max_value = np.max(data)
                if min_value == 0:
                    min_value = 0.01 # avoiding division by zero when defining logarithmic bins
                    data = [d + 0.01 if d==0 else d for d in data] # adding a small jitter to 0 values to include them in the histogram
                bins = network_analysis.get_log_bins(min_value, max_value, nbins)
                plt.xscale('log')

            ax.hist(data, bins, color=color, rwidth=bar_width)

            ax.set_xlabel('Number of nodes/links of type {}'.format(key))
            ax.set_ylabel('Count')
            plt.tight_layout()

            if save_path_base:
                assert len(save_name) > 0, 'Please give file name for saving the node and link type histograms'
                save_path = save_path_base + '/' + save_name + '_' + key + '.pdf'
                plt.savefig(save_path, format='pdf', bbox_inches='tight')
                plt.close()
            else:
                plt.show()
                plt.close()

