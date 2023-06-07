import sys
import os
import unittest
import re

testdir = os.path.dirname(__file__)
srcdir = '../app'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from tools import generate_text, calculate_result, calculate_cwpm
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))

punct = re.compile(r"[^\w\s]")
ru = re.compile(r"[^A-Яа-я\s]")
en = re.compile(r"[^A-Za-z\s]")

class TestGenTest(unittest.TestCase):

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

class TestCalcResult(unittest.TestCase):

    def setUp(self):
        self.test_text = '''
            King added in a furious passion and went back to
        '''

    def test_0_0(self):
        user_text = ""
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 0)

    def test_1_some_val(self):
        user_text = "King added in a furious"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 50)

    def test_2_wrong_case(self):
        user_text = "king added in a furious"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 40)

    def test_3_some_mistakes(self):
        user_text = "king adde In a furious and went back to"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 20)


    def test_4_perfect(self):
        user_text = self.test_text
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 100)


class TestCalcCWPM(unittest.TestCase):

    def setUp(self):
        self.test_text = '''
            King added in a furious passion and went back to
        '''

    def test_0_0(self):
        user_text = ""
        res = calculate_cwpm(self.test_text, user_text, 10)
        self.assertEqual(res, 0)

    def test_1_some_val_10(self):
        user_text = "King added in a furious"
        res = calculate_cwpm(self.test_text, user_text, 10)
        self.assertEqual(res, 30)

    def test_2_some_val_30(self):
        user_text = "King added in a furious"
        res = calculate_cwpm(self.test_text, user_text, 30)
        self.assertEqual(res, 10)

    def test_3_some_val_60(self):
        user_text = "King added in a furious"
        res = calculate_cwpm(self.test_text, user_text, 60)
        self.assertEqual(res, 5)

    def test_4_wrong_case(self):
        user_text = "king added in a furious"
        res = calculate_cwpm(self.test_text, user_text, 5)
        self.assertEqual(res, 48)

    def test_5_some_mistakes(self):
        user_text = "king adde In a furious and went back to"
        res = calculate_cwpm(self.test_text, user_text, 20)
        self.assertEqual(res, 6)


    def test_6_perfect(self):
        user_text = self.test_text
        res = calculate_cwpm(self.test_text, user_text, 60)
        self.assertEqual(res, 10)


