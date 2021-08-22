#!/usr/bin/env python

"""Tests for `raytracer` package."""


import unittest
from click.testing import CliRunner

from raytracer import cli
from raytracer.geometry import Triangle
from raytracer.vector import Vector


class TestRaytracer(unittest.TestCase):
    """Tests for `raytracer` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'raytracer.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


class TestVector(unittest.TestCase):

    def test_equals(self):
        assert Vector(1, 3, 2) == Vector(1, 3, 2)
        assert Vector(1, 2, 3) != Vector(0, 2, 1)

    def test_addition(self):
        assert Vector(1, 1, 1) + Vector(5, 3, 2) == Vector(6, 4, 3)
        assert Vector(10, -18, 9) + Vector(3, -34, 9) == Vector(13, -52, 18)

    def test_subtraction(self):
        assert Vector(1, 1, 1) - Vector(-3, -4, 3) == Vector(4, 5, -2)

    def test_multiplication(self):
        assert Vector(3, 4, 5) * 2 == Vector(6, 8, 10)
        assert Vector(4, 2, 0) * Vector (0, 0, 3) == 0
        assert Vector(4, 2, 8) ** 2 == 84

    def test_matmul(self):
        assert Vector(1, 2, 3) @ Vector(1, 5, 7) == Vector(-1, -4, 3)
        assert Vector(-1, -2, 3) @ Vector(4, 0, -8) == Vector(16, 4, 8)


class TestTriangle(unittest.TestCase):

    def test_intersect_fine(self):
        t = Triangle(Vector(1, 0, 0),
                     Vector(0, 1, 0),
                     Vector(0, 0, 1))

        assert t.contains(Vector(0.28, 0.23, 0.49))

    def test_intersect_coarse(self):
        t = Triangle(Vector(1, 0, 0),
                     Vector(0, 1, 0),
                     Vector(0, 0, 1))

        v = Vector(-0.14, 0.52, 0.62)
        assert t.check_coarse(v)
        assert not t.check_fine(v)

