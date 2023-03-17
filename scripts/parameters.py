# Parameters for the Climate Watch project

# data and network construction
data_folder = '/home/onerva/projects/climate_watch/data'
municipality_tags = ['helsinki-kierto', 'helsinki-kierto-2023','espoo-ilmasto','tampere-ilmasto+tampere-lumo','lpr-ilmasto+lpr-kierto','lahti-ilmasto','akaa-ilmasto','valkeakoski-ilmasto','palkane-ilmasto','urjala-ilmasto','hame-ilmasto','hsy-kestava','aanekoski-yio','viitasaari-ilmasto','leichlingen-klima','stpaul-carp','boroondara-cap','indigoshire-erp']
municipality_name_key = ['organization','name']
action_key = 'actions'
action_attributes = ['name','description','schedule','implementationPhase','responsibleParties','categories','contactPersons','updatedAt']
action_to_action_link_key = 'relatedActions'
indicator_level_key = 'indicatorLevels'
indicator_type_key = 'level'
indicator_key = 'indicator'
indicator_attributes = ['name','organization','categories','maxValue','minValue','latestValue']
action_to_indicator_link_key ='relatedActions'
action_neighbour_key ='action'
indicator_to_indicator_link_key ='relatedCauses'
indicator_neighbour_key ='causalIndicator'

# network analysis
node_type_key = 'node_type'
node_types = ['action', 'indicator_OPERATIONAL', 'indicator_TACTICAL', 'indicator_STRATEGIC', 'indicator']
projection_graph_spanning_node_types = ['action']
n_degree_bins = 5
n_type_histogram_bins = 10
n_projection_graph_density_bins = 5
node_and_link_type_histogram_bin_type = 'logarithmic'
projection_graph_density_bin_type = 'linear'


# visualization
full_network_layout = 'graphviz'
projection_graph_layout = 'graphviz'
node_colors = {'action':'b','indicator_OPERATIONAL':'g','indicator_TACTICAL':'c','indicator_STRATEGIC':'m','indicator':'k'}
node_markers = {'action':'o','indicator_OPERATIONAL':'s','indicator_TACTICAL':'d','indicator_STRATEGIC':'*','indicator':'.'}
node_size = 15
edge_width = 0.7
edge_alpha = 0.5
arrow_size = 5
line_style = '-'
line_width = '1.5'
distribution_alpha = 0.5
hist_bar_width = 0.75

save_path_base = '/home/onerva/projects/climate_watch/results/'
network_vis_save_name = 'network'
degree_dists_save_name = 'degree_distributions'
node_and_link_type_histograms_save_name = 'type_histogram'
projection_graph_vis_save_name = 'projection-graph'
projection_graph_density_histogram_save_name = 'projection_graph_density'
