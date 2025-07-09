# 3D Rendering Engine

A Python-based 3D rendering engine using PyOpenGL and Pygame, featuring modular control system and OBJ model loading.

## Features

- Wireframe rendering of 3D models
- OBJ file format support
- Modular control system architecture
- Camera controls:
  - WASD/Arrow keys: Move camera
  - Mouse drag: Rotate view
  - Mouse wheel: Zoom
  - Q/E: Move forward/backward
  - R: Reset view

## Installation

1. Clone the repository:
```bash
git clone git@github.com:algorsnipes99/3d-rendeder.git
cd 3d-rendeder
```

2. Install dependencies:
```bash
pip install pygame PyOpenGL numpy
```

## Usage

Run the engine:
```bash
python main.py
```

Controls:
- **Movement**: WASD or Arrow keys
- **Rotation**: Left mouse button + drag
- **Zoom**: Mouse wheel
- **Reset View**: R key

## Architecture

### Core Components
- `main.py`: Entry point and game loop
- `render_matrix.py`: Vertex/edge data structure
- `renderer.py`: OpenGL rendering logic
- `obj_importer.py`: OBJ file loader

### Control System
- `controls/base_controls.py`: Abstract base class
- `controls/control_processor.py`: Event delegation
- `controls/basic_movement.py`: Camera controls

## Example Models

The project includes:
- `cube.obj`: Simple test cube

## Future Enhancements
- Solid rendering modes
- Lighting support
- Texture mapping
- Additional control schemes
