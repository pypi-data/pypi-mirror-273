# tests/test_visualizer.py

import unittest
from codeviz import visualize_code

class TestVisualizer(unittest.TestCase):
    def test_visualize_code(self):
        fig = visualize_code('sample.py')
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()