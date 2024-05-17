import unittest
import numpy as np
from picture2pixel import process_image, apply_floyd_steinberg_dithering, generate_verilog_code

class TestPicture2Pixel(unittest.TestCase):

    def test_process_image(self):
        reconstructed_image = process_image('https://www.comp.nus.edu.sg/~guoyi/project/picture2pixel/default.png', 96, 64, 20)
        self.assertEqual(reconstructed_image.shape, (64, 96, 3))

    def test_apply_floyd_steinberg_dithering(self):
        image = np.zeros((64, 96, 3), dtype=np.uint8)
        dithered_image = apply_floyd_steinberg_dithering(image)
        self.assertEqual(dithered_image.shape, (64, 96, 3))

    def test_generate_verilog_code(self):
        pixels = np.zeros((64 * 96, 3), dtype=np.uint8)
        verilog_code = generate_verilog_code(pixels)
        self.assertIn("else oled_data = 0;", verilog_code)

if __name__ == '__main__':
    unittest.main()
