from unittest import TestCase, main

from frontend.constants import PROJECT_PATH


class TestInit(TestCase):
    def test_path(self):
        self.assertTrue(PROJECT_PATH.exists())
        self.assertIn("frontend", str(PROJECT_PATH))


if __name__ == "__main__":
    main()
