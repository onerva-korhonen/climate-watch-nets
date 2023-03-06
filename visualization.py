# functions for visualization

import matplotlib.pylab as plt
import networkx as nx

from collections import Counter

def draw_network(G, node_type_key='node_type', node_colors={}, node_markers={}, node_size=50, edge_width=1, edge_alpha=0.5, save_path_base='', save_name=''):
    """
    Visualizes the network and saves the plot as pdf. If save path is not given, the figure is shown instead of saving.

    Parameters:
    -----------
    G: networkx.graph(), the network to be visualized
    node_type_key: str, key under which the attribute node type is stored in G.nodes
    node_colors: dict, color of each node type (keys: node types)
    node_markers: dict, marker of each node type (keys: node types)
    node_size: scalar, node size in the visualization
    edge_widht: dbl or str, width of network edges, set to 'weight' to use individual edge weights
    edge_alpha: dbl, opacity of edges
    save_path_base: str, a base path (e.g. to a shared folder) for saving figures
    save_name: str, name of the file where to save the network visualization

    Returns:
    --------
    No direct output, saves the network visualization as pdf
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    pos = nx.spring_layout(G)
    nodes = G.nodes(data=True)
    # reading node types
    assert Counter(node_colors.keys()) == Counter(node_markers.keys()), "Node color and marker keys don't match, check the keys!"
    node_types = set(node_colors.keys())
    
    # drawing nodes of each type separately
    for node_type in node_types:
        nodes_to_add = []
        for node in nodes:
            if node[1][node_type_key] == node_type:
                nodes_to_add.append(node[0])
        nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=nodes_to_add, node_color=node_colors[node_type], node_shape=node_markers[node_type], node_size=node_size,label=node_type)
    
    # drawing edges
    if edge_width == 'weight':
        edges = list(G.edges())
        weights = [G[edge[0]][edge[1]]['weight'] for edge in edges]
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, width=weights, alpha=edge_alpha)
    else:
        edges = list(G.edges())
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, width=edge_width, alpha=edge_alpha)

    # saving network
    if save_path_base:
        assert len(save_name)>0, 'Give a file name for saving the visualization!'
        save_path = save_path_base + '/' + save_name
        plt.savefig(save_path, format='pdf', bbox_inches='tight')
        plt.close()
    else:
        plt.show()
        plt.close()






