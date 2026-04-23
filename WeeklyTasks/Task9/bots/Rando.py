from random import choice

class Rando(object):
	def update(self, gameinfo):
		# will only atack if we have available plantes and targets
		if gameinfo._my_planets() and gameinfo._not_my_planets():
			# will randomly select a source and destination planet from the available planets
			dest = choice(list(gameinfo._not_my_planets().values()))
			src = choice(list(gameinfo._my_planets().values())) 
			if src.ships > 10: # will only luanch if the amount of ships in the planet is more than 10
				gameinfo.planet_order(src, dest, int(src.ships * 0.75))