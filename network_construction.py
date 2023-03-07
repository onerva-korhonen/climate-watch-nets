# functions for reading data and constructing networks

import json
import operator
from functools import reduce
from unidecode import unidecode
import networkx as nx

def read_municipality_data(base_path, municipality_tag, municipality_name_key=['organization','name'], action_key='actions', action_attributes=[], indicator_level_key='indicatorLevels', indicator_type_key='level',indicator_key='indicator',indicator_attributes=[],action_to_action_link_key='relatedActions',action_to_indicator_link_key='relatedActions',action_neighbour_key='action',indicator_to_indicator_link_key='relatedCauses',indicator_neighbour_key='causalIndicator'):
    """
    Reads the climate actions and indicators of a municipality
    from .json file. Links of indicators are read downwards: actions and
    other indicators contributing to each indicator are listed as neighbours
    and link direction follows the order of hierarcy (from actions to lower-level
    indicators to higher-level indicators). Links between actions are read for 
    each action and duplicates are removed (i.e. only link a-b is listed 
    and b-a removed).

    Parameters:
    -----------
    base_path: str, path of the folder containing the .json files
    municipality_tag: str, identificator of the municipality whose data to read. Tags of the format
                      'municipality1+municipality2+...+municipalityN' allow combining data from multiple
                      municipalities
    municipality_name_key: list of strs, keys under which the municipality name is stored
                           in the data; the format is nested: municipality name is stored
                           in the data at data[municipality_name_key[0]][municipality_name_key[1]] etc.
    action_key: str, key under which actions are stored in the data
    action_attributes: list of strs, attributes of actions to be read
                      from the .json file and to be included in the network
                      construction as node attributes
    indicator_level_key: str, key under which indicators are stored in the data
    indicator_type_key: str, key under which the indicator type is stored in the data
    indicator_key: str, key under which each indicator is stored inside indicator level;
                   the format is nested: indicator attributes are stored at 
                   data[indicator_level_key][i][indicator][indicator_attribute]
    indicator_attributes: list of strs, attributes of indicators to be read
                          from the .json file and to be included in the
                          network construction as node attributes
    action_to_action_link_key: str, key under which the related actions are stored
    action_to_indicator_link_key: str, key under which the actions contributing to each indicator are
                                  stored
    action_neighbour_key: str, key under which the information about neighbouring actions is stored
    indicator_to_indicator_link_key: str, key under which the indicators hierarchically contributing
                                     to each indicator are stored
    indicator_neighbour_key: str, key under with the information about neighbouring indicators is stored

    Returns:
    --------
    nodes: list of dictionaries in format {node_id:{attribute_name:attribute_value}}
    links: list in edge list format (list of pairs of nodes)
    municipality_name: str, name of the municipality; used later
                       for saving the network

    TODO: consider the possibility of giving all keys as params
    """
    municipality_tags = municipality_tag.split('+')
    if len(municipality_tags) > 1:
        print('Merging {} .json files'.format(len(municipality_tags)))
    
    municipality_names = []
    nodes = []
    links = []

    for municipality_tag in municipality_tags:
        path = base_path + '/' + municipality_tag + '.json'
        f = open(path)
        data = json.load(f)
        f.close()
    
        # the outermost keys reflect the database structure of the Kausal Watch
        data = data['data']['plan']
        # reading municipality name and removing spaces, diacritics, and capitals
        if municipality_name_key[0] in data.keys():
            municipality_name = reduce(operator.getitem, municipality_name_key, data)
            municipality_name = municipality_name.replace(' ', '_')
            municipality_name = unidecode(municipality_name).lower()
            municipality_names.append(municipality_name)
            print('Municipality name {}'.format(municipality_name))
            print('Project name {}'.format(data['name']))
        else:
            municipality_name = ''
            print('No municipality name detected in the data, check municipality_name_key')

        # reading node and link information

        if action_key in data.keys():
            actions = data[action_key]
            a2a_links = action_to_action_link_key in actions[0].keys() # checking if there are action-action links
            n_a2a = 0
            for action in actions:
                aid = action['id']
                node_attributes = {action_attribute:action[action_attribute] for action_attribute in action_attributes}
                node_attributes['node_type'] = 'action'
                nodes.append({aid:node_attributes})
                # reading link information from actions
                if a2a_links:
                    neighbours = action[action_to_action_link_key]
                    for neighbour in neighbours:
                        if (aid,neighbour['id']) not in links and (neighbour['id'],aid) not in links:
                            links.append((action['id'],neighbour['id']))
                            n_a2a += 1
            print('{} actions found'.format(len(actions)))
            if a2a_links:
                 print('{} links from actions to actions found'.format(n_a2a))
            else:
                print('No links from actions to actions found, check action to action link key!')
        else:
            print('No actions found, check the action key!')

        if indicator_level_key in data.keys():
            indicators = data[indicator_level_key]
            print('{} indicators found'.format(len(indicators)))
            if len(indicators) > 0:
                a2i_links = action_to_indicator_link_key in indicators[0][indicator_key].keys() # checking if there are action-to-indicator links
                i2i_links = indicator_to_indicator_link_key in indicators[0][indicator_key].keys() # checking if there are action-to-action links
                n_a2i = 0
                n_i2i = 0
                for indicator in indicators:
                    if indicator_type_key in indicator.keys():
                        node_type = 'indicator_{}'.format(indicator[indicator_type_key])
                    else:
                        node_type = 'indicator'
                    indicator = indicator[indicator_key]
                    iid = indicator['id']
                    node_attributes = {indicator_attribute:indicator[indicator_attribute] for indicator_attribute in indicator_attributes}
                    node_attributes['node_type'] = node_type
                    nodes.append({iid:node_attributes})
                    # reading link information from indicators
                    if a2i_links:
                        neighbours = indicator[action_to_indicator_link_key]
                        for neighbour in neighbours:
                            links.append((neighbour[action_neighbour_key]['id'],iid))
                        n_a2i += len(neighbours) 
                    if i2i_links:
                        neighbours = indicator[indicator_to_indicator_link_key]
                        for neighbour in neighbours:
                            links.append((neighbour[indicator_neighbour_key]['id'],iid))
                        n_i2i += len(neighbours)
                if a2i_links:
                    print('{} links from actions to indicators found'.format(n_a2i))
                else:
                    print('No links from actions to indicators found, check action to indicator link key!')
                if i2i_links:
                    print('{} links from indicators to indicators found'.format(n_i2i))
                else:
                    print('No links from indicators to indicators found, check indicator to indicator link key')
        else:
            print('No indicators found, check the indicator key!')
    
    municipality_names = set(municipality_names)
    if len(municipality_names) > 1:
        municipality_name = '+'.join(municipality_names)
    else:
        municipality_name = municipality_names.pop()

    return nodes, links, municipality_name

def construct_network(nodes, links, municipality_name='', save_path_base=''):
    """
    Constructs a networkx graph object from given nodes and links and saves it to a file if wanted. Note that the current version saves the network as an edgelist that doesn't preserve node attributes.

    Parameters:
    -----------
    nodes: list of dictionaries in format {node_id:{attribute_name:attribute_value}}
    links: list in edge list format (list of pairs of nodes)
    municipality_name: str, name of the municipality, used for saving the network
    save_path_base: str, base path to which save the network

    Returns:
    --------
    G: a networkx graph object
    """
    G = nx.DiGraph()
    node_ids = []
    for node in nodes:
        node_ids.extend([i for i in node])
    G.add_nodes_from(node_ids)
    G.add_edges_from(links)
    # TODO: setting the attributes could be done with set_node_attributes in networkx 3, consider upgrading
    for node, node_id in zip(nodes, node_ids):
        node_attributes = node[node_id]
        for attribute in node_attributes:
            G.nodes[node_id][attribute] = node_attributes[attribute]
    # TODO: .edg doesn't preserve node attributes; consider saving as pickle in networkx 3
    if save_path_base:
        save_path = save_path_base + '/' + municipality_name + '.edg'
        nx.write_edg(G, save_path)
    return G




