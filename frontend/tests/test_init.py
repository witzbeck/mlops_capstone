from unittest import TestCase, main

from __init__ import path
from frontend.constants import PROJECT_PATH


class TestInit(TestCase):
    def test_path(self):
        self.assertTrue(PROJECT_PATH.exists())
        self.assertIn("frontend", str(PROJECT_PATH))
        self.assertIn(str(PROJECT_PATH), path)


if __name__ == "__main__":
    main()
