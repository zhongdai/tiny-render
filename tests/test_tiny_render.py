import os
import unittest
from datetime import datetime
from tempfile import TemporaryDirectory
from unittest import mock

from tiny_render import __version__
from tiny_render import Render


class TestTinyRender(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        print(f"tempdir: {self.tempdir.name}")

        os.environ["TEST_ENV"] = "abc"

    def tearDown(self):
        self.tempdir.cleanup()
        del os.environ["TEST_ENV"]

    def test_dir_not_exist(self):
        with self.assertRaises(ValueError):
            _ = Render("non/exist/path")

    def test_render(self):
        with open(os.path.join(self.tempdir.name, "test.txt"), "w") as f:
            f.write("hello {{key}}")

        params = {"key": "world"}

        r = Render(self.tempdir.name)

        self.assertEqual("hello world", r.go("test.txt", **params))

    @mock.patch.object(Render, "get_shortsha")
    def test_gitsha_with_params(self, mocked_method):
        mocked_method.return_value = "1234567"

        with open(os.path.join(self.tempdir.name, "test.txt"), "w") as f:
            f.write("gitshar: {{_gitsha}}, hello {{key}}")

        params = {"key": "world"}

        r = Render(self.tempdir.name)

        self.assertEqual("gitshar: 1234567, hello world", r.go("test.txt", **params))

    @mock.patch.object(Render, "get_shortsha")
    def test_gitsha_only(self, mocked_method):
        mocked_method.return_value = "1234567"

        with open(os.path.join(self.tempdir.name, "test.txt"), "w") as f:
            f.write("gitshar: {{_gitsha}}")

        r = Render(self.tempdir.name)

        self.assertEqual("gitshar: 1234567", r.go("test.txt"))

    def test_getenv(self):
        with open(os.path.join(self.tempdir.name, "test.txt"), "w") as f:
            f.write("hello {{ 'TEST_ENV' | getenv}}")

        r = Render(self.tempdir.name)

        self.assertEqual("hello abc", r.go("test.txt"))

    def test_date_time(self):
        """cannot mock the built-in class, so only to parse the return"""
        with open(os.path.join(self.tempdir.name, "test.txt"), "w") as f:
            f.write("{{ _date_str }},{{ _time_str }}")

        r = Render(self.tempdir.name)
        _d, _t = r.go("test.txt").split(",")

        _date = datetime.strptime(_d, "%Y%m%d")
        _datetime = datetime.strptime(_t, "%Y%m%d%H%M%S")

        self.assertTrue(isinstance(_date, datetime))
        self.assertTrue(isinstance(_datetime, datetime))
