import json
import networkx as nx
import time
import pathlib
import tempfile

ENV = "test"
FAHRWEG_GRAPHEN_ENDPOINT_URL = f"https://flux{ENV}.app.ose.sbb-cloud.net/backend/fahrweg/" \
                               f"preprocessedLineareAbschnittsfolgen"


def from_node_id(route_path, route_section, index_in_path):
    if "route_alternative_marker_at_entry" in route_section.keys() and \
            route_section["route_alternative_marker_at_entry"] is not None and \
            len(route_section["route_alternative_marker_at_entry"]) > 0:
                return "(" + str(route_section["route_alternative_marker_at_entry"][0]) + ")"

    else:
        if index_in_path == 0:  # can only get here if this node is a very beginning of a route
            return "(" + str(route_section["sequence_number"]) + "_beginning)"
        else:
            return "(" + (str(route_path["route_sections"][index_in_path - 1]["sequence_number"]) + "->" +
                          str(route_section["sequence_number"])) + ")"


def to_node_id(route_path, route_section, index_in_path):
    if "route_alternative_markers_at_exit" in route_section.keys() and \
            route_section["route_alternative_markers_at_exit"] is not None and \
            len(route_section["route_alternative_markers_at_exit"]) > 0:

                return "(" + str(route_section["route_alternative_markers_at_exit"][0]) + ")"
    else:
        if index_in_path == (len(route_path["route_sections"]) - 1): # meaning this node is a very end of a route
            return "(" + str(route_section["sequence_number"]) + "_end" + ")"
        else:
            return "(" + (str(route_section["sequence_number"]) + "->" +
                          str(route_path["route_sections"][index_in_path + 1]["sequence_number"])) + ")"

def generate_fahrweg_graphen(verkehrsplan):
    start_time = time.time()

    # now build the graph. Nodes are called "previous_FAB -> next_FAB" within lineare abschnittsfolgen and "AK" if
    # there is an Abschnittskennzeichen 'AK' on it
    fahrweg_graphen = dict()
    for route in scenario["routes"]:

        # set global graph settings
        G = nx.DiGraph(route_id = route["id"],
                       name="Route-Graph for route "+route["id"])

        # add edges with data contained in the preprocessed graph
        for path in route["route_paths"]:
            for (i, route_section) in enumerate(path["route_sections"]):
                G.add_edge(from_node_id(path, route_section, i),
                           to_node_id(path, route_section, i),
                           abschnittsfolge_id=path["id"],
                           **route_section)

        # enrich with data not contained the preprocessed graph, only in the original verkehrsplan
        for (u, v, data) in G.edges.data():
            fahrweg_id = G.graph["fahrweg_id"]
            fabs_from_verkehrsplan = fahrwege_from_verkehrsplan_lookup_dict[fahrweg_id]
            data.update(fabs_from_verkehrsplan[data["sequence_number"]])

        fahrweg_graphen[route["faId"]] = G

    print(str(time.time() - start_time) + " finished building fahrweg-graphen")
    return fahrweg_graphen


# scratch######################################

scenario = "../sample_files/sample_scenario_with_routing_alternatives_eng.json"
with open(scenario) as fp:
    scenario = json.load(fp)