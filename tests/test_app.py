from unittest import TestCase

from app import app

class TestApp(TestCase):
    def test_app(self):
        self.assertIsNotNone(app)
