class Tactical(object):
	def update(self, gameinfo):
		my = gameinfo._my_planets()
		enemy = gameinfo._enemy_planets()
		neutral = gameinfo._neutral_planets()
		
		if not my:
			return
		
		# defensive moment
		for fleet in gameinfo._enemy_fleets().values():
			if fleet.dest.ID in my:
				# detect when a my plante is under attack
				dest = fleet.dest
				src = min(my.values(), key=lambda p: p.distance_to(dest))
				if src.ships > 10 and src.ID != dest.ID:
					gameinfo.planet_order(src, dest, int(src.ships * 0.75))
				return 
		
		# attack moment
		targets = enemy if enemy else neutral
		if not targets:
			return
		
		src = max(my.values(), key=lambda p: p.ships)
		dest = min(targets.values(), key=lambda p: p.ships)
		
		if src.ships > 10:
			gameinfo.planet_order(src, dest, int(src.ships * 0.75))