import sys
import os
import unittest
import re

testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from app import generate_text
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))

punct = re.compile(r"[^\w\s]")
ru = re.compile(r"[^A-Яа-я\s]")
en = re.compile(r"[^A-Za-z\s]")

class TestGenTest(unittest.TestCase):
    """Класс тестов генерации текста"""

    def test_0_ru(self):
        text = generate_text("ru", 10, False)
        self.assertFalse(re.findall(ru, text))

    def test_1_en(self):
        text = generate_text("en", 10, False)
        self.assertFalse(re.findall(en, text))

    def test_2_10(self):
        text = generate_text("ru", 10, False)
        self.assertEqual(len(text.split()), 10)

    def test_3_40(self):
        text = generate_text("ru", 40, False)
        self.assertEqual(len(text.split()), 40)

    def test_4_100(self):
        text = generate_text("ru", 100, False)
        self.assertEqual(len(text.split()), 100)
    
    def test_5_false(self):
        text = generate_text("ru", 10, False)
        self.assertFalse(re.findall(punct, text))

    def test_6_true(self):
        text = generate_text("ru", 10, True)
        self.assertTrue(re.findall(punct, text))
