import os
import numpy as np
from picture2pixel import process_image, apply_floyd_steinberg_dithering, generate_verilog_code

def picture_to_pixel(filename, width, height, svd_r, output_dir):
    # Process the image
    image = process_image(filename, width, height, svd_r)
    
    # Apply dithering
    processed_image = apply_floyd_steinberg_dithering(image)
    
    # Generate Verilog code
    pixels = processed_image.reshape(-1, 3)
    verilog_code = generate_verilog_code(pixels)

    # Output results
    if output_dir == 0:
        print(verilog_code)
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        output_file = os.path.join(output_dir, f"{base_filename}.p2p")
        with open(output_file, 'w') as f:
            f.write(verilog_code)
    
    return processed_image

# Example usage
if __name__ == "__main__":
    picture_to_pixel("https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/default.png", 96, 64, 20, 0)
