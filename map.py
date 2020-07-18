"""
Author: Jack Lonnborn
Date: June 2019

This program reads in data about people (and animals) moving in and out of 
different houses, and creates a graph connecting people who have lived together. 
The nodes of the graph are people (animals), and an edge connecting two nodes is 
colour-coded by the house that those two people lived in together.
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from classes import *

save_flag = True
img_filename = "example"  # saves a pdf and png
input_filename = "data.txt"


def get_people(entry):
    """
	Splits up a `people in` (`people out`) entry in an input line 
	to extract each comma-separated person moving in (out).
	"""
    try:
        return entry.split(",")
    except ValueError:
        return entry


def make_Person(name):
    """
	Makes a new Person if not yet in the list `people`
	"""
    if not name in (p.name for p in people):
        new_person = Person(name)
        people.append(new_person)
        return new_person


def make_House(name):
    """
	Makes a new House if not yet in the list `houses`
	"""
    if not name in (h.name for h in houses):
        new_house = House(name)
        houses.append(new_house)
        return new_house


def get_or_make_obj(name, ls, obj_type):
    """
	Fetches an object from a list of objects based on its name, or creates an
	object of type `obj_type` if one of that name doesn't already exist
	"""
    obj = next((i for i in ls if i.name == name), None)
    if obj is None:
        if obj_type == "person":
            obj = make_Person(name)
        elif obj_type == "house":
            obj = make_House(name)
    return obj


def make_edge_colours(houses):
    """
	Constructs a dictionary of house names with associated colours, 
	for colouring edges in the graph.
	"""
    colours_vec = [
        "#003f5c",
        "#2f4b7c",
        "#665191",
        "#a05195",
        "#d45087",
        "#f95d6a",
        "#ff7c43",
        "#ffa600",
        "#7f95d1",
        "#ffc0be",
        "#488f31",
        "#2ca25f",
        "#fdbb84",
    ]
    colours = {house.name: colour for house, colour in zip(houses, colours_vec)}
    return colours


def make_network():
    """
	Constructs a graph with
	nodes: all people appearing in the input data;
	edges: between people who have lived together.
	"""
    G = nx.MultiGraph()
    colours = make_edge_colours(houses)
    for person in people:
        G.add_node(person.id)
    for person in people:
        for c in person.connections:
            G.add_edge(person.id, c[0], color=colours[c[1]])
    return G


def get_node_labels(G):
    """
	Returns dicts of the position and labels of all nodes in the graph.
	"""
    pos = nx.spring_layout(G)
    labels = {}
    for node in G.nodes():
        # find the name associated with the id attached to this node:
        name = next((i.name for i in people if i.id == node))
        labels[node] = name
    return pos, labels


def make_legend_artists(clr, **kwargs):
    """
	Generates coloured lines for the graph legend.
	"""
    return Line2D([0, 1], [0, 1], color=clr, **kwargs)


people = []
houses = []


def main():
    with open(input_filename, "r") as f:
        next(f)
        for line in f:
            data = line.strip().split(";")

            house = get_or_make_obj(data[0], houses, "house")
            people_in = get_people(data[1])
            people_out = get_people(data[2])

            for person_name in people_in:
                p = get_or_make_obj(person_name, people, "person")
                house.change_occupants(p, add=True)
            for person_name in people_out:
                p = get_or_make_obj(person_name, people, "person")
                house.change_occupants(p, add=False)

            house.update_connections()

    dash = get_or_make_obj("-", people, "person")
    people.remove(dash)

    G = make_network()
    colours_dict = make_edge_colours(houses)
    colours = [G[u][v][0]["color"] for u, v in G.edges()]
    pos, labels = get_node_labels(G)

    fig = plt.figure(figsize=(20, 20))

    # use nx.draw with invisible nodes/edges to add the graph to matplotlib `fig`.
    # this is necessary to later set the facecolor
    nx.draw(G, pos, node_color="#4b4b4b", edge_color="#4b4b4b")

    # add the nodes, node labels (i.e. people's names), and colour-coded edges:
    nx.draw_networkx_nodes(G, pos, alpha=0.3, facecolor="#4b4b4b")
    nx.draw_networkx_labels(
        G,
        pos,
        labels,
        font_size=10,
        font_color="white",
        font_weight="normal",
        facecolor="#4b4b4b",
    )
    e = nx.draw_networkx_edges(G, pos=pos, edge_color=colours, facecolor="#4b4b4b")

    # make the legend
    # adapted from:
    # https://stackoverflow.com/questions/48065567/legend-based-on-edge-color-in-networkx
    leg_artists = [make_legend_artists(clr, lw=5) for clr in colours_dict.values()]
    leg_labels = ["{}".format(house) for house in colours_dict.keys()]
    plt.legend(leg_artists, leg_labels)

    fig.set_facecolor("#4b4b4b")

    if save_flag:
        plt.savefig("{}.pdf".format(img_filename), facecolor="#4b4b4b")
        plt.savefig("{}.png".format(img_filename), facecolor="#4b4b4b")
    else:
        plt.show()


if __name__ == "__main__":
    main()
