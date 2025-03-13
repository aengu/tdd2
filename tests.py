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

"""
unittest.TestCase랑 django.test.TestCase 차이점 중 하나
- 각 테스트케이스가 설정된 Isolation lev에 따라 트랜잭션으로 진행됨
- 테스트 실행 전후로 자동으로 테스트db 설정/초기화
"""