# A script for constructing networks from data downloaded from the Climate Watch API

# importing network_construction with importlib to ensure that it's imported from the right path
import importlib.util
spec = importlib.util.spec_from_file_location('network_construction','/home/onerva/projects/climate_watch/climate-watch-nets/network_construction.py')
nc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nc)

spec = importlib.util.spec_from_file_location('parameters','/home/onerva/projects/climate_watch/climate-watch-nets/scripts/parameters.py')
params = importlib.util.module_from_spec(spec)
spec.loader.exec_module(params)

path_base = params.data_folder
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

for municipality_tag in municipality_tags:
    path = path_base + '/' + municipality_tag + '.json'
    nodes,links,_ = nc.read_municipality_data(path, municipality_name_key=municipality_name_key, action_key=action_key, action_attributes=action_attributes, indicator_level_key=indicator_level_key, indicator_type_key=indicator_type_key, indicator_key=indicator_key, indicator_attributes=indicator_attributes, action_to_indicator_link_key=action_to_indicator_link_key, action_neighbour_key= action_neighbour_key, indicator_to_indicator_link_key=indicator_to_indicator_link_key, indicator_neighbour_key=indicator_neighbour_key)
    _ = nc.construct_network(nodes, links, municipality_tag, save_path_base=path_base)
