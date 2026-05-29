
In this project I had to do target simulation with a predictive point, using four different weapons. The simulation runs an attacker that stands still, shooting at a 
patrolling target calculating its interception points

## Features
- **Predictive Aiming**: Using quadratic formula to solve the interception poinr from the shooting target to the moving one.
- **Weapon Profiles**: Rifle, Rocket, Handgun, Grenade with different speeds and accuracy.
- **Hit Detection**: Target flashes red on impact (I recommend to switch to a slower firing rate weapon, because Rifle shoots too fast to notice change colour)
- **Weapon Switching**: Change weapons during simulation.

## Key Bindings on Modes have been deleted for consisterncy and bug fixing (explained in PDF report)

## Weapon Profiles Key bindings

1. Rifle: R key, 800 speed, high accuracy, 4 bullets per second fire rate, yellow color
2. Rocket, O key, 300 speed, high accuracy, 1 bullets per second fire rate, orange color
3. Handgun, H key, 700 speed, low accuracy, 3 bullets per second fire rate, grey color
4. Grenade, G key, 200 speed, low accuracy, 0.7 bullets per second fire rate, green color

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
