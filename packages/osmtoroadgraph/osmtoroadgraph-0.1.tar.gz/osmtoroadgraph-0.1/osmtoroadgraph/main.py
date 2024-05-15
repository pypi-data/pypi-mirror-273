import os
import importlib.util

import configuration as config
import osm.read_osm
import osm.sanitize_input
import output.write_graph as output

from graph import contract_graph, convert_graph, algorithms, graphfactory
from utils import timer

# Example usage
# from osm_to_roadgraph import convert_osm_to_roadgraph
# convert_osm_to_roadgraph('path/to/file.osm', 'p', lcc=False, contract=True, networkx_output=True)
@timer.timer
def convert_osm_to_roadgraph(filename, network_type, lcc=True, contract=False, networkx_output=False):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"provided filename {filename} does not point to a file!")
    
    long_network_type = {"p": "pedestrian", "c": "car", "b": "bicycle"}
    network_type = long_network_type.get(network_type, network_type)
    if network_type not in long_network_type.values():
        raise ValueError("network type improperly set")

    configuration = config.Configuration(network_type)

    r_index = filename.rfind(".")
    out_file = filename[:r_index]

    print(f"selected network type: {configuration.network_type}")
    print(f"accepted highway tags: {configuration.accepted_highways}")
    print(f"opening file: {filename}")

    nodes, ways = osm.read_osm.read_file(filename, configuration)

    osm.sanitize_input.sanitize_input(ways, nodes)

    graph = graphfactory.build_graph_from_osm(nodes, ways)

    if lcc:
        graph = algorithms.computeLCCGraph(graph)

    output.write_to_file(graph, out_file, configuration.get_file_extension())

    if networkx_output:
        if importlib.util.find_spec("networkx") is None:
            raise ImportError("networkx Library not found. Please install networkx to use the networkx output option.")
        
        nx_graph = convert_graph.convert_to_networkx(graph)
        output.write_nx_to_file(nx_graph, f"{out_file}.json")

    if contract:
        contracted_graph = contract_graph.ContractGraph(graph).contract()
        output.write_to_file(
            contracted_graph, out_file, f"{configuration.get_file_extension()}c"
        )
        if networkx_output:
            nx_graph = convert_graph.convert_to_networkx(contracted_graph)
            output.write_nx_to_file(nx_graph, f"{out_file}_contracted.json")
