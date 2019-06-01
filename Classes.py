import itertools
import sys

class Person():
	"""
	A Person object collects `connections` to people who live in the same House at the same time. These connections form the edges of the network.

	"""
	newid = itertools.count()
	def __init__(self, name):
		self.id = next(Person.newid)
		self.name = name
		self.houses = []
		self.connections = []

class House():
	"""
	A House has a name (e.g. it's address), and a list of occupants. The occupants change when people move in or out.
	"""
	def __init__(self, name):
		self.name = name		# a label, e.g. an address
		self.occupants = [] 	# list of people currently in the house

	def change_occupants(self, person, add):
		"""
		Adds or removes someone from the house
		"""
		if person.name=="-":
			pass
		elif add:
			person.houses.append(self.name)
			self.occupants.append(person)
		elif not add:
			try:
				self.occupants.remove(person)
			except ValueError:
				sys.exit("Tried to remove {}, who wasn't a member of {}! Check your input data for errors.".format(person.name, self.name))

	def update_connections(self):
		"""
		Creates connections between current housemates.
		Called after a line of input data has been processed.
		"""
		for housemate in self.occupants:
			c = housemate.connections
			for hm in self.occupants:
				if housemate.name != hm.name:
					c.append((hm.id, self.name))
			c = list(set(c)) # remove duplicates
			housemate.connections = c
