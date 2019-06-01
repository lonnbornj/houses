import networkx as nx
import matplotlib.pyplot as plt
from Classes import *

plt.close()

def get_people(entry):
	"""
	Splits up an `people in` or `people_out` entry in an input line to extract each comma-separated person.
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
	obj = next((i for i in ls if i.name == name), None)
	if obj is None:
		if obj_type=="person":
			obj = make_Person(name)
		elif obj_type=="house":
			obj = make_House(name)
	return obj

def make_edge_colours(houses):
	"""
	Constructs a dictionary of house names with associated colours, for colouring edges in the graph.
	Colours are from: https://learnui.design/tools/data-color-picker.html
	"""
	colours_vec = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
	colours = {house.name: colour for house, colour in zip(houses, colours_vec)}
	return colours

def make_network():
	"""
	Constructs a graph with
	nodes: all people appearing in the input data;
	edges: between people who have lived together
	"""
	G = nx.MultiGraph()
	colours=make_edge_colours(houses)
	for person in people:
		G.add_node(person.id)
	for person in people:
		for c in person.connections:
			G.add_edge(person.id, c[0], color=colours[c[1]])
	return G

def get_node_labels(G):
	"""
	Returns the position and labels of all nodes in the graph
	"""
	pos = nx.spring_layout(G)
	labels={}
	for node in G.nodes():
		name = next((i.name for i in people if i.id == node))
		labels[node] = name
	return pos, labels

people = []
houses = []

def main():
	with open("data.txt", "r") as f:
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
	colours = [G[u][v][0]['color'] for u,v in G.edges()]
	pos, labels = get_node_labels(G)

	fig = plt.figure()
	nx.draw_networkx_nodes(G, pos, alpha=0.3)
	nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='white', font_weight='normal')
	nx.draw(G, pos, edge_color=colours)
	fig.set_facecolor("#4b4b4b")
	plt.show()

if __name__=="__main__":
	main()