'''  BoxWorldWindow to test/demo graph (path) search.

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>, James Bonner <jbonner@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

See readme.txt for details.

'''

import sys
import pyglet
#importing graphics for side-effects - it creates the egi and window module objects. 
#This is the closest python has to a global variable and it's completely gross
import graphics
#game has to take another approach to exporting a global variable
#the game object is importable, but only contains the game object if it's being imported after the game object has been created below
import game

# TASK 6: Update function for agent movement
def update(dt):
	if game.game:
		game.game.update(dt)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "task6_map.txt"  # Default to Task 6 map

	game.game = game.Game(filename)
    
	#update func task 6
	pyglet.clock.schedule_interval(update, 1/60.0)
    
	pyglet.app.run()