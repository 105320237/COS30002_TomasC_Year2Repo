class BestWorst(object):
	def update(self, gameinfo):
		# will only atack if we have available plantes and targets
		if gameinfo._my_planets() and gameinfo._not_my_planets():
			
            # will select the planet with the most ships as source and the planet with the least ships as destination
			src = max(gameinfo._my_planets().values(), key=lambda p: p.ships)
			
			dest = min(gameinfo._not_my_planets().values(), key=lambda p: p.ships)
			if src.ships > 10: # will only luanch if the amount of ships in the planet is more than 10
				gameinfo.planet_order(src, dest, int(src.ships * 0.75))