## Features

- **Cohesion**: Agents move towards the average position of their neighbours
- **Separation**: Agents move away from neighbours to avoid visual bugs and crampment
- **Alignment**: Agents match the heading movement of their neighbours
- **Weighted-Sum Blending**: All the furces sum up for a single vector movement
- **Real time weight modifications**: Adjust weights live with keyboard controls
- **On Screen Display**: Current weight values shown at all times

## Key Bindings

- `0`: Flock Mode (all agents)
- `1`: Seek Mode
- `2`: Arrive Slow
- `3`: Arrive Normal
- `4`: Arrive Fast
- `5`: Flee Mode
- `8`: Wander Mode
- `F`: Spawn a new Agent
- `I`: Toggle Debug Information (Vectors and Info)
- `P`: Pause/Resume

### Weight Tuning Keys

**Cohesion:**
- `Z`: Decrease
- `X`: Increase

**Separation:**
- `C`: Decrease
- `V`: Increase

**Alignment:**
- `B`: Decrease
- `N`: Increase

**Wander:**
- `M`: Decrease
- `,`: Increase

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
