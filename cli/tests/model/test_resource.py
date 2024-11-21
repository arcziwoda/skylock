"""
Module to test the Resource model.
"""

import unittest
from skylock_cli.model.resource import Resource


class TestResource(unittest.TestCase):
    """
    Test cases for the Resource model.
    """

    def test_resource_default_state(self):
        """
        Test the default state of a Resource instance.
        """
        resource = Resource()
        self.assertFalse(resource.is_public)
        self.assertEqual(resource.visibility_label, "private 🔐")
        self.assertEqual(resource.visibility_color, "red")

    def test_resource_public_state_from_init(self):
        """
        Test the public state of a Resource instance from the init method.
        """
        resource = Resource(is_public=True)
        self.assertTrue(resource.is_public)
        self.assertEqual(resource.visibility_label, "public 🔓")
        self.assertEqual(resource.visibility_color, "green")

    def test_make_public(self):
        """
        Test the make_public method.
        """
        resource = Resource()
        resource.make_public()
        self.assertTrue(resource.is_public)
        self.assertEqual(resource.visibility_label, "public 🔓")
        self.assertEqual(resource.visibility_color, "green")

    def test_make_private(self):
        """
        Test the make_private method.
        """
        resource = Resource()
        resource.make_public()  # First make it public
        resource.make_private()  # Then make it private again
        self.assertFalse(resource.is_public)
        self.assertEqual(resource.visibility_label, "private 🔐")
        self.assertEqual(resource.visibility_color, "red")


if __name__ == "__main__":
    unittest.main()
