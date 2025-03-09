from apps import Superhero
import unittest

# python -m unittest tests.py

class TestSuperhero(unittest.TestCase):
    def setUp(self):
        self.superhero = Superhero(name="Superman", strength_level=50)

    def test_stringfy(self):
        self.assertEqual(str(self.superhero), "Superman")
    
    def test_is_stronger_than_other_hero(self):
        other_superhero = Superhero(name="Batman", strength_level=100)
        self.assertFalse(self.superhero.is_stronger_than(other_superhero))