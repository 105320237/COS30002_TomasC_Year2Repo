# Box World Navigation Visualiser

A sandbox tool to visualise how Graph Searching algorithms navigate 2D grid worlds.

### Authorship
- **Original Author**: Created for COS30002 AI for Games by Clinton Woodward (cwoodward@swin.edu.au).
- **Updated and Maintained by**: Enrique Ketterer (ekettererortiz@swin.edu.au).

## Objective
To understand Depth First Search (DFS), Breadth First Search (BFS), Dijkstra's, and A* Search algorithms applied to a simple "box" based world.

## Features
- Interactive grid where tiles can be changed (clear, mud, water, wall, forest, road).
- Configurable start and target positions.
- Multiple search algorithms:
  - Breadth First Search (BFS)
  - Depth First Search (DFS)
  - Dijkstra's Algorithm
  - A* (AStar) Search
- Step-by-step limits for clear instructional visualisation.
- Navigation graph, search tree, and final path overlaid visually.
- Fully compatible with Pyglet 2.0+ library updates.
- Four autonomous agent types with unique navigation behaviours (Task 6).

## Features CHANGES By Tomas (Task 5)
- Changed min_edge_cost from 10.0 to 1.0 in box_world.py
- Uncommented diagonal edge code in box_world.py
- Selected the active heuristic to _hypot() instead of _manhattan()
- The Euclidean distance is better for diagonal movement estimates.

## Features ADDED By Tomas (Task 6)
- Added two new terrain types: Forest (key 7) and Road (key 8).
- Implemented four moving agent types: Ground, Flying, Tank, and Car.
- Each agent builds its own navigation graph with unique cost rules.
- Agents follow calculated paths at constant speed with visual path lines.
- Full agent lifecycle controls: spawn, target, select, pause, and reset.

## Parameters/Flags
Run the tool by passing the map file path directly via the CLI:
`python main.py [map_filename]`

Example maps include `map1.txt`, `map2.txt`, and `task6_map.txt` which come pre-configured.

## Usage Examples
`uv run main.py map1.txt`
Loads the visualiser using the configuration specified in `map1.txt`.

`uv run main.py task6_map.txt`
Loads the larger 20x15 world with all six terrain types and agent support.

## Agent Usage (Task 6)
If you want to set the experiment, press A, then G, then click somewhere to spawn a Ground agent. In case you want to spawn more, you can follow the same instructions but change the G to an F/K/V key for other agents. If you have more than one Agent spawned, you can select the current Agent to create a target by pressing TAB, then, press Y and click on an available tile. You can press O to pause/resume all agents, and R to reset them to their spawn points.

### Controls
The world's boxes can be changed by selecting the box "kind" and left-clicking onto a box.

**Tile Brushes:**
- **1**: "clear" (white)
- **2**: "mud" (grey-brownish)
- **3**: "water" (blue)
- **4**: "wall" (black)
- **7**: "forest" (green)
- **8**: "road" (light grey)

**Node Placement:**
- **5**: "start"
- **6**: "target"

**Execution & Limits:**
- **SPACE**: force a replan (execute search)
- **N / M**: Cycle (backward/forward) through the search methods and replan.
- **UP / DOWN**: Increase or decrease the search step depth limit by one.
- **0**: Remove the search step limit (A full search will be performed).

**Visibility Toggles:**
- **E**: toggle edges on/off for the current navigation graph (thin blue lines)
- **L**: toggle box (node) index values on/off (useful for understanding search and path details).
- **C**: toggle box "centre" markers on/off
- **T**: toggle tree on/off for the current search if available
- **P**: toggle path on/off for the current search if there is a successful route.

**Agent Controls (Task 6):**
- **A**: Toggle agent spawn mode ON/OFF
- **G**: Select Ground agent (yellow, normal terrain costs)
- **F**: Select Flying agent (blue, ignores terrain costs)
- **K**: Select Tank agent (orange, double terrain costs)
- **V**: Select Car agent (pink, prefers roads)
- **Y**: Enter target mode (click on a tile to set target for selected agent)
- **TAB**: Cycle through spawned agents
- **O**: Pause/Resume all agents
- **R**: Reset all agents to their spawn points

## Installation
Requires Python 3.13+ and Pyglet 2.0+.
Install via `uv` or `pip`:
`uv sync`