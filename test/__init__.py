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

class TestGenTest(unittest.TestCase):

    def test_0_ru_10_false(self):
        text = generate_text("ru", 10, False)
        self.assertEqual(len(text.split()), 10)
        self.assertFalse(re.findall(punct, text))
        self.assertFalse(re.findall(ru, text))
