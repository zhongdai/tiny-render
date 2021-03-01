
import unittest

from tiny_render import Render
from tiny_render import __version__

class TestTinyRender(unittest.TestCase):
    def setUp(self):
        pass

    def test_dir_not_exist(self):
         with self.assertRaises(ValueError):
             _ = Render("non/exist/path")

