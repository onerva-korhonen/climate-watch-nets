# A frontend script for running analysis and producing visualizations
# For a script for reading the data and constructing networks, see
# construct_networks.py

import networkx as nx

# importing modules from climate-watch-nets with importlib to ensure that it's imported from the right path
import importlib.util

spec = importlib.util.spec_from_file_location('parameters','/home/onerva/projects/climate_watch/climate-watch-nets/scripts/parameters.py')
params = importlib.util.module_from_spec(spec)
spec.loader.exec_module(params)

spec = importlib.util.spec_from_file_location('network_construction','/home/onerva/projects/climate_watch/climate-watch-nets/network_construction.py')
nc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nc)

spec = importlib.util.spec_from_file_location('network_analysis','/home/onerva/projects/climate_watch/climate-watch-nets/network_analysis.py')
na = importlib.util.module_from_spec(spec)
spec.loader.exec_module(na)

spec = importlib.util.spec_from_file_location('visualization','/home/onerva/projects/climate_watch/climate-watch-nets/visualization.py')
vis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vis)

data_folder = params.data_folder
municipality_tags = params.municipality_tags
#municipality_tags = ['helsinki-kierto']
municipality_name_key = params.municipality_name_key
action_key = params.action_key
action_attributes = params.action_attributes
action_to_action_link_key = params.action_to_action_link_key
indicator_level_key = params.indicator_level_key
indicator_type_key = params.indicator_type_key
indicator_key = params.indicator_key
indicator_attributes = params.indicator_attributes
action_to_indicator_link_key = params.action_to_indicator_link_key
action_neighbour_key = params.action_neighbour_key
indicator_to_indicator_link_key = params.indicator_to_indicator_link_key
indicator_neighbour_key = params.indicator_neighbour_key

node_type_key = params.node_type_key
node_types = params.node_types
projection_graph_spanning_node_types = params.projection_graph_spanning_node_types
n_degree_bins = params.n_degree_bins
n_type_histogram_bins = params.n_type_histogram_bins
n_projection_graph_density_bins = params.n_projection_graph_density_bins
node_and_link_type_histogram_bin_type = params.node_and_link_type_histogram_bin_type
projection_graph_density_bin_type = params.projection_graph_density_bin_type

full_network_layout = params.full_network_layout
projection_graph_layout = params.projection_graph_layout
node_colors = params.node_colors
node_markers = params.node_markers
node_size = params.node_size
edge_width = params.edge_width
edge_alpha = params.edge_alpha
arrow_size = params.arrow_size
line_style = params.line_style
line_width = params.line_width
distribution_alpha = params.distribution_alpha
hist_bar_width = params.hist_bar_width

save_path_base = params.save_path_base
network_vis_save_base = params.network_vis_save_name
degree_dists_save_base = params.degree_dists_save_name
node_and_link_type_histograms_save_base = params.node_and_link_type_histograms_save_name
projection_graph_vis_save_base = params.projection_graph_vis_save_name
projection_graph_density_histogram_save_name = params.projection_graph_density_histogram_save_name

degree_dists_per_node_type = [[] for node_type in node_types]

counts = {}
projection_graph_densities = [[] for spanning_node_type in projection_graph_spanning_node_types]
projection_graph_densities_without_linkless = [[] for spanning_node_type in projection_graph_spanning_node_types]

for municipality_tag in municipality_tags:
    nodes,links,_ = nc.read_municipality_data(data_folder, municipality_tag, municipality_name_key=municipality_name_key, action_key=action_key, action_attributes=action_attributes, indicator_level_key=indicator_level_key, indicator_type_key=indicator_type_key, indicator_key=indicator_key, indicator_attributes=indicator_attributes, action_to_indicator_link_key=action_to_indicator_link_key, action_neighbour_key= action_neighbour_key, indicator_to_indicator_link_key=indicator_to_indicator_link_key, indicator_neighbour_key=indicator_neighbour_key)
    G = nc.construct_network(nodes, links, municipality_tag)
    network_vis_save_name = network_vis_save_base + '_' + municipality_tag + '.pdf'
    vis.draw_network(G, layout=full_network_layout, node_type_key=node_type_key, node_colors=node_colors, node_markers=node_markers, node_size=node_size, edge_width=edge_width, edge_alpha=edge_alpha, arrow_size=arrow_size, save_path_base=save_path_base, save_name=network_vis_save_name)
    degree_dists = na.calculate_degree_distributions(G, node_types, node_type_key, n_degree_bins)
    for degree_dist_per_node_type, degree_dist in zip(degree_dists_per_node_type, degree_dists):
        if len(degree_dist[0]) > 0:
            degree_dist_per_node_type.append(degree_dist)
    count = na.count_node_and_link_types(G, node_types, node_type_key)
    for key in count:
        if key in counts.keys():
            counts[key].append(count[key])
        else:
            counts[key] = [count[key]]
    for i, spanning_node_type in enumerate(projection_graph_spanning_node_types):
        action_graph = nc.create_projection_graph(G,spanning_node_type,node_type_key) # TODO: add saving of projection graphs?
        projection_graph_densities[i].append(nx.density(action_graph))
        projection_graph_densities_without_linkless[i].append(na.calculate_density_without_linkless_nodes(G))
        action_graph_vis_save_name = projection_graph_vis_save_base + '_' + spanning_node_type + '_' + municipality_tag + '.pdf'
        vis.draw_network(action_graph, layout=projection_graph_layout, node_type_key=node_type_key, node_colors=node_colors, node_markers=node_markers, node_size=node_size, edge_width=edge_width, edge_alpha=edge_alpha, save_path_base=save_path_base, save_name=action_graph_vis_save_name)

for degree_dist_per_node_type, node_type in zip(degree_dists_per_node_type, node_types):
    if len(degree_dist_per_node_type) > 0:
        save_path = save_path_base + '/' + degree_dists_save_base + '_' + node_type + '.pdf'
        vis.plot_curves(degree_dist_per_node_type, normalize=False, x_label='Degree', y_label='PDF', colors=node_colors[node_type], line_style=line_style, line_width=line_width, alpha=distribution_alpha, save_path=save_path)
        # re-plotting degree distributions with normalized x axis. Note that for municipalities where all nodes have degree 0, this leads to negative x values
        save_path = save_path_base + '/' + degree_dists_save_base + '_' + node_type + '_normalized.pdf'
        vis.plot_curves(degree_dist_per_node_type, normalize=True, x_label='Degree', y_label='PDF', colors=node_colors[node_type], line_style=line_style, line_width=line_width, alpha=distribution_alpha, save_path=save_path)

vis.visualize_node_and_link_type_count(counts, bin_type=node_and_link_type_histogram_bin_type, nbins=n_type_histogram_bins, bar_width=hist_bar_width, save_path_base=save_path_base, save_name=node_and_link_type_histograms_save_base)

for spanning_node_type, density, density_without_linkless in zip(projection_graph_spanning_node_types, projection_graph_densities, projection_graph_densities_without_linkless):
    save_path = save_path_base + '/' + projection_graph_density_histogram_save_name + '_' + spanning_node_type + '.pdf'
    vis.create_histogram(density, bin_type=projection_graph_density_bin_type, nbins=n_projection_graph_density_bins, bar_width=hist_bar_width, x_label='Density', y_label='Count', save_path=save_path)
    print('Projection graph densities for spanning node type {}:'.format(spanning_node_type))
    print(density)

    save_path = save_path_base + '/' + projection_graph_density_histogram_save_name + '_without_linkless_' + spanning_node_type + '.pdf'
    vis.create_histogram(density_without_linkless, bin_type=projection_graph_density_bin_type, nbins=n_projection_graph_density_bins, bar_width=hist_bar_width, x_label='Density', y_label='Count', save_path=save_path)
    print('Projection graph densities for spanning node type {}, only nodes with degree > 0:'.format(spanning_node_type))
    print(density_without_linkless)
