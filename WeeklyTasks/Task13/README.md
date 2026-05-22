# Autonomous Agent Steering - Lab 12

This project is a pedagogical simulation of autonomous agent steering behaviours using Python and the Pyglet library. It demonstrates fundamental AI concepts such as Seek, Flee, Arrive, Wander, and Path Following.

## Features
- **Steering Behaviours**: Implementations for Seek, Arrive (Slow/Normal/Fast), and placeholders for Flee, Pursuit, Wander, and Path Following.
- **Visual Telemetry**: Real-time visualization of steering forces, velocity, and desired changes using color-coded vectors.
- **Toroidal World**: Agents wrap around screen boundaries for continuous movement.
- **Interactive Controls**: Move the target with the mouse and change agent modes via keyboard.

## Key Bindings
- `1`: Seek Mode
- `2`: Arrive Slow
- `3`: Arrive Normal
- `4`: Arrive Fast
- `5`: Flee Mode
- `6`: Pursuit Mode
- `7`: Follow Path Mode
- `8`: Wander Mode
- `A`: Spawn a new Agent
- `R`: Randomise path waypoints
- `H`: Set the first agent only as a pursuit Target
- `M`: Cycle FIRST agent's mode independently
- `P`: Pause/Resume Simulation
- `I`: Toggle Debug Information (Vectors and Info Batch)

## TASK 12 CHANGES 

## SPECIFIC INSTRUCTIONS FOR PURSUIT TESTING
    Creating the pursuit mode was somewhat challenging, since activating it would make all the Agents in sight to work within the same "mode",
    so when activating pursuit, none of the Agents would focus on the Target, so I had to change the way that Agents are managed. When you press "H", the first Agent is set as the pursuit target (the evader that others will chase). Pressing "M" cycles the first agent's mode independently, allowing you to set it to Seek so it follows the star while other agents chase The first Agent.

1. Press "A" until you have 2 Agents on screen
2. Press "H" to set the first Agent as the pursuit target
3. Press "M" for the first Agent to switch to Seek (looking for the star target)
4. Press "6" to make the second Agent go into Pursuit mode

## Changes made

- Path following, which makes Agents follow random generated waypoints.
- Path Reset, which Generates new random waypoints for the Agents
- Wander, which gives a random wandering movement set by a target on a circle
- Agent Cycling, to independently switch the FIRST agent's mode to test the "hunter/evader" scenario
- Force limit, max_force prevents too much "snapping" or aggressive jitter for the steering motion
- Pursuit, seeks towards a future poisition to intercept target.

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
