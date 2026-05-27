# Autonomous Agent Steering - Lab 13

## Features
- **Hide Feature**: Prey calculates possible hiding spots behind obstacles.
- **Wander Feature**: Hunter moves randomly.
- **Visuals**: X markers to show all hiding spots.

## Key Bindings
- `0`: Hide mode (All Agents)
- `1`: Seek mode
- `2`: Arrive Slow
- `3`: Arrive Normal
- `4`: Arrive Fast
- `5`: Flee Mode
- `8`: Wander Mode
- `A`: Spawn a new Agent
- `I`: Toggle debug visuals
- `P`: Pause/Resume

## TASK 12 CHANGES 

## Changes from Task 12

- **Removed**: Path following, pursuit, and related key bindings (6, 7, R, H, M)
- **Added**: Hide behaviour with geometric hiding spot calculation
- **Added**: Three circular obstacles in the environment
- **Added**: X markers for hiding spot visualisation
- **Modified**: Game spawns hunter and prey with distinct visuals and physics


## Technical Requirements
- Python 3.13+
- Pyglet 2.1.14+

## Installation
Ensure you have the dependencies installed:
```bash
uv add pyglet
```

## Attribution
- Original code by Clinton Woodward, James Bonner, and Steve Dower.
- Comments and code refactored by **Enrique Ketterer** <ekettererortiz@swin.edu.au> - S1 2026.
