# Autonomous Agent Steering - Lab 12

Layered Finite State Machine simulation. A soldier patrols waypoints, detects enemies,
switches to attack mode, shoots, reloads, and returns to patrol.

## Features
- **Layered FSM**: uses high-level for patrol and attack, and low-level for Seek, Arrive, Shoot, Reload states
- **Patrol**: Soldier follows waypoints using seek and arrive behaviours
- **Attack**: Soldier detects enemies, aims, shoots, and reloads when out of ammo
- **Health System**: Enemies have health, die after taking enough damage
- **Weapon Switching**: Weapon switching feature from task 15

## Key Bindings

- `E`: Spawn enemy at random position
- `R`: Rifle, fast, accurate
- `O`: Rocket, slow, accurate
- `H`: Handgun, fast, inaccurate
- `G`: Grenade, slow, inaccurate
- `P`: Pause/Resume

## How It Works

1. Soldier patrols a square path of four waypoints.
2. Press E to spawn a stationary red enemy.
3. If enemy is within detection range, FSM switches from Patrol to Attack.
4. Soldier shoots until ammo runs out, reloads, and continues.
5. When enemy dies, soldier returns to patrol.
6. Switch weapons anytime with R, O, H, G.

## Technical Requirements
- Python 3.13+
- Pyglet 2.1.14+

## Installation
Ensure you have the dependencies installed:
```bash
uv add pyglet
```