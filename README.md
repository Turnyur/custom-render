
# Custom 3D Object Renderer

This repository contains a custom renderer I implemented as part of my ongoing [3D Reconstruction / Supersizing project](#), which I will make public later. I used this renderer to visualize 3D objects, such as those from ShapeNet and Objaverse, from various views and different azimuthal and rotational angles. See [Perspective Camera Toy](https://ksimek.github.io/perspective_camera_toy.html).

## ToDo
I primarily used the renderer in a way that is closely coupled with my project structure and expectations. However, I intend to generalize the renderer to be more versatile in the future. The goal is to allow users to render scenes from different perspectives by adjusting azimuthal and rotational angles. It will support models from popular datasets like ShapeNet and Objaverse.

---

## Features

- Render 3D objects from ShapeNet, Objaverse, and similar datasets
- Customize views by adjusting azimuthal and rotational angles
- High-quality rendering output
- Easy parameter customization

## Installation

Clone the repo. and install the necessary dependencies:

```bash
git clone https://github.com/Turnyur/custom-render.git
cd custom-render
pip install -r requirements.txt
```

## Usage

### Rendering 3D Objects/Scene

To render a 3D object, use:

```bash
python render.py --input path/to/3d/object --output path/rendered/image_category --azimuth 30 --elevation 45
```

### Configuration

Configure various parameters for the rendering process:

- `--input`: Path to object category (WordNet Synset ID)
- `--output`: Desired output directory
- `--azimuth`: Azimuthal angle for the view (in degrees) 
- `--elevation`: Elevation angle for the view (in degrees)
- `--distance`: Distance from the camera to the object (z-axis)
- `--resolution`: Resolution of the output image (width x height)

For a full list of configurable options, run:

```bash
python render.py --help
```

______


Full description coming soon.
_______