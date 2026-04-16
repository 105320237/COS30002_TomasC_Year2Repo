game = None

from enum import Enum
import pyglet
from box_world import BoxWorld, search_modes
from graphics import window

# Mouse mode indicates what the mouse "click" should do...
class MouseModes(Enum):
	CLEAR =		pyglet.window.key._1
	MUD =		pyglet.window.key._2
	WATER =		pyglet.window.key._3
	WALL =		pyglet.window.key._4
	START =		pyglet.window.key._5
	TARGET =	pyglet.window.key._6
	FOREST =	pyglet.window.key._7
	ROAD =		pyglet.window.key._8

class SearchModes(Enum):
	DFS =		1
	BFS =		2
	Dijkstra =	3
	AStar =		4

class Game():
	def __init__(self, map):
		self.world = BoxWorld.FromFile(map)
		self.mouse_mode = MouseModes.MUD
		window._update_label('mouse', 'Click to place: '+self.mouse_mode.name)

		self.search_mode = 1
		window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
		self.search_limit = 0
		window._update_label('status', 'Status: Loaded')
		
		# AGENT MANAGEMENT (Task 6)
		self.selected_agent = None
		self.agent_spawn_mode = False
		self.agent_target_mode = False
		self.agent_spawn_type = "ground"
		window._update_label('agent', 'Agents: 0 | A:Add G:Ground F:Flying K:Tank V:Car Y:Target TAB:Cycle O:Pause')

	def plan_path(self):
		self.world.plan_path(self.search_mode, self.search_limit)
		window._update_label('status', 'Status: Path Planned')
	
	def update(self, dt):
		'''Update agents each frame.'''
		self.world.update_agents(dt)
		window._update_label('agent', f'Agents: {len(self.world.agents)} | A:Add G:Ground F:Flying K:Tank V:Car Y:Target TAB:Cycle O:Pause')

	def input_mouse(self, x, y, button, modifiers):
		box = self.world.get_box_by_pos(x, y)
		if not box:
			return
			
		if self.agent_target_mode and self.selected_agent:
			self.selected_agent.set_target(box.index)
			self.agent_target_mode = False
			window._update_label('status', f'Status: Agent {self.selected_agent.agent_id} target set to {box.index}')
			return
			
		if self.agent_spawn_mode:
			self.world.add_agent(self.agent_spawn_type, box.index)
			self.agent_spawn_mode = False
			window._update_label('status', f'Status: {self.agent_spawn_type.upper()} agent spawned at {box.index}')
			return
			
		if self.mouse_mode == MouseModes.START:
			self.world.set_start(box.node.idx)
		elif self.mouse_mode == MouseModes.TARGET:
			self.world.set_target(box.node.idx)
		else:
			box.set_type(self.mouse_mode.name)
		self.world.reset_navgraph()
		self.plan_path()
		window._update_label('status', 'Status: Graph Changed')

	def input_keyboard(self, symbol, modifiers):
		if symbol in [m.value for m in MouseModes]:
			for mode in MouseModes:
				if mode.value == symbol:
					self.mouse_mode = mode
					window._update_label('mouse', 'Click to place: '+self.mouse_mode.name)
					break

		elif symbol == pyglet.window.key.M:
			self.search_mode += 1
			if self.search_mode > len(search_modes):
				self.search_mode = 1
			self.world.plan_path(self.search_mode, self.search_limit)
			window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
			
		elif symbol == pyglet.window.key.N:
			self.search_mode -= 1
			if self.search_mode <= 0:
				self.search_mode = len(search_modes)
			self.world.plan_path(self.search_mode, self.search_limit)
			window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
			
		elif symbol == pyglet.window.key.SPACE:
			self.world.plan_path(self.search_mode, self.search_limit)
			
		elif symbol == pyglet.window.key.UP:
			self.search_limit += 1
			window._update_label('status', 'Status: limit=%d' % self.search_limit)
			self.world.plan_path(self.search_mode, self.search_limit)
			
		elif symbol == pyglet.window.key.DOWN:
			if self.search_limit > 0:
				self.search_limit -= 1
				window._update_label('status', 'Status: limit=%d' % self.search_limit)
				self.world.plan_path(self.search_mode, self.search_limit)
				
		elif symbol == pyglet.window.key._0:
			self.search_limit = 0
			window._update_label('status', 'Status: limit=%d' % self.search_limit)
			self.world.plan_path(self.search_mode, self.search_limit)
		
		# AGENT CONTROLS (Task 6)
		elif symbol == pyglet.window.key.A:
			self.agent_spawn_mode = not self.agent_spawn_mode
			self.agent_target_mode = False
			status = "ON" if self.agent_spawn_mode else "OFF"
			window._update_label('status', f'Status: Agent spawn mode {status} (Type: {self.agent_spawn_type.upper()})')
			
		elif symbol == pyglet.window.key.G:
			self.agent_spawn_type = "ground"
			window._update_label('status', 'Status: Spawn type = GROUND (respects terrain)')
			
		elif symbol == pyglet.window.key.F:
			self.agent_spawn_type = "flying"
			window._update_label('status', 'Status: Spawn type = FLYING (ignores terrain)')
			
		elif symbol == pyglet.window.key.K:
			self.agent_spawn_type = "tank"
			window._update_label('status', 'Status: Spawn type = TANK (slow, double costs)')
			
		elif symbol == pyglet.window.key.V:
			self.agent_spawn_type = "car"
			window._update_label('status', 'Status: Spawn type = CAR (fast, prefers roads)')
			
		elif symbol == pyglet.window.key.Y:
			if self.world.agents:
				self.agent_target_mode = True
				self.agent_spawn_mode = False
				window._update_label('status', 'Status: Click to set target for selected agent')
			else:
				window._update_label('status', 'Status: No agents to target')
				
		elif symbol == pyglet.window.key.TAB:
			if self.world.agents:
				if self.selected_agent is None:
					self.selected_agent = self.world.agents[0]
				else:
					idx = self.world.agents.index(self.selected_agent)
					idx = (idx + 1) % len(self.world.agents)
					self.selected_agent = self.world.agents[idx]
				agent_type = "GROUND"
				if type(self.selected_agent).__name__ == "FlyingAgent":
					agent_type = "FLYING"
				elif type(self.selected_agent).__name__ == "TankAgent":
					agent_type = "TANK"
				elif type(self.selected_agent).__name__ == "CarAgent":
					agent_type = "CAR"
				window._update_label('status', f'Status: Selected Agent {self.selected_agent.agent_id} ({agent_type})')
			else:
				window._update_label('status', 'Status: No agents available')
				
		elif symbol == pyglet.window.key.O:
			if self.world.agents:
				for agent in self.world.agents:
					agent.active = not agent.active
				status = "PAUSED" if not self.world.agents[0].active else "RESUMED"
				window._update_label('status', f'Status: Agents {status}')
			else:
				window._update_label('status', 'Status: No agents to pause')
				
		elif symbol == pyglet.window.key.R:
			self.world.reset_agents()
			self.selected_agent = None
			window._update_label('status', 'Status: Agents reset to start positions')