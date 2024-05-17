# picture2pixel

`picture2pixel` is a Python package for processing images and generating Verilog code for FPGA.

## Installation

You can install `picture2pixel` using pip:

pip install picture2pixel


## Usage

Here's an example of how to use `picture2pixel`:

```python
from picture2pixel.main import picture_to_pixel

# Process the image and generate Verilog code
processed_image = picture_to_pixel('https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/default.png', 96, 64, 20, 0)
