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

spec = importlib.util.spec_from_file_location('visualization','/home/onerva/projects/climate_watch/climate-watch-nets/visualization.py')
vis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vis)

data_folder = params.data_folder
municipality_tags = params.municipality_tags
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
node_colors = params.node_colors
node_markers = params.node_markers
node_size = params.node_size
edge_width = params.edge_width
edge_alpha = params.edge_alpha

save_path_base = params.save_path_base
network_vis_save_base = params.network_vis_save_name

for municipality_tag in municipality_tags:
    nodes,links,_ = nc.read_municipality_data(data_folder, municipality_tag, municipality_name_key=municipality_name_key, action_key=action_key, action_attributes=action_attributes, indicator_level_key=indicator_level_key, indicator_type_key=indicator_type_key, indicator_key=indicator_key, indicator_attributes=indicator_attributes, action_to_indicator_link_key=action_to_indicator_link_key, action_neighbour_key= action_neighbour_key, indicator_to_indicator_link_key=indicator_to_indicator_link_key, indicator_neighbour_key=indicator_neighbour_key)
    G = nc.construct_network(nodes, links, municipality_tag)
    network_vis_save_name = network_vis_save_base + '_' + municipality_tag + '.pdf'
    vis.draw_network(G, node_type_key=node_type_key, node_colors=node_colors, node_markers=node_markers, node_size=node_size, edge_width=edge_width, edge_alpha=edge_alpha, save_path_base=save_path_base, save_name=network_vis_save_name)
