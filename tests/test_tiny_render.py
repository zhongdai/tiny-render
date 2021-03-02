
import os
from tempfile import TemporaryDirectory
import unittest
from unittest import mock



from tiny_render import Render
from tiny_render import __version__

class TestTinyRender(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        print(f"tempdir: {self.tempdir.name}")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_dir_not_exist(self):
         with self.assertRaises(ValueError):
             _ = Render("non/exist/path")

    def test_render(self):
        with open(os.path.join(self.tempdir.name,"test.txt"), 'w') as f:
            f.write("hello {{key}}")

        params = {"key": "world"}

        r = Render(self.tempdir.name)

        self.assertEqual("hello world", r.go("test.txt", **params))


    @mock.patch.object(Render, 'get_shortsha')
    def test_gitsha_with_params(self, mocked_method):
        mocked_method.return_value = "1234567"

        with open(os.path.join(self.tempdir.name,"test.txt"), 'w') as f:
            f.write("gitshar: {{_gitsha}}, hello {{key}}")

        params = {"key": "world"}

        r = Render(self.tempdir.name)

        self.assertEqual("gitshar: 1234567, hello world", r.go("test.txt", **params))


    @mock.patch.object(Render, 'get_shortsha')
    def test_gitsha_only(self, mocked_method):
        mocked_method.return_value = "1234567"

        with open(os.path.join(self.tempdir.name,"test.txt"), 'w') as f:
            f.write("gitshar: {{_gitsha}}")

        r = Render(self.tempdir.name)

        self.assertEqual("gitshar: 1234567", r.go("test.txt"))