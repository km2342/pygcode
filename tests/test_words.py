import unittest

# Add relative pygcode to path
from .testutils import add_pygcode_to_path
add_pygcode_to_path()

# Units under test
from pygcode import words
from pygcode import dialects


class WordIterTests(unittest.TestCase):
    def test_iter1(self):
        block_str = 'G01 Z-0.5123456789 Y-0.511111423 X-3.234e+4 F100 Z1.5 Z-1 Y-1 Z-1.752e-12 Y-1.752e-12'
        w = list(words.text2words(block_str, xy_decimals=5))
        # word length
        self.assertEqual(len(w), 10)
        self.assertEqual(w[0].value_str, words.Word('G', 1).value_str)
        self.assertEqual(w[1].value_str, words.Word('Z', -0.512, xy_decimals=5).value_str)
        self.assertEqual(w[2].value_str, words.Word('Y', -0.51111, xy_decimals=5).value_str)
        self.assertEqual(w[3].value_str, words.Word('X', -32340.00000, xy_decimals=5).value_str)
        self.assertEqual(w[4].value_str, words.Word('F', 100).value_str)
        self.assertEqual(w[5].value_str, words.Word('Z', 1.5).value_str)
        self.assertEqual(w[6].value_str, words.Word('Z', -1).value_str)
        self.assertEqual(w[7].value_str, words.Word('Y', -1.00000).value_str)
        # testing for scientific notation in non x and y letters
        self.assertEqual(w[8].value_str, words.Word('Z', .000).value_str)
        # testing for duplicate negative signs in X string
        self.assertEqual(w[9].value_str, words.Word('Y', .000).value_str)

    def test_iter2(self):
        block_str = 'G02 X10.75 Y47.44 I-0.11 J-1.26 F70'
        w = list(words.text2words(block_str))
        # word length
        self.assertEqual(len(w), 6)
        # word values
        self.assertEqual([w[0].letter, w[0].value], ['G', 2])
        self.assertEqual([w[1].letter, w[1].value], ['X', 10.75])
        self.assertEqual([w[2].letter, w[2].value], ['Y', 47.44])
        self.assertEqual([w[3].letter, w[3].value], ['I', -0.11])
        self.assertEqual([w[4].letter, w[4].value], ['J', -1.26])
        self.assertEqual([w[5].letter, w[5].value], ['F', 70])


class WordValueMatchTest(unittest.TestCase):
    def regex_assertions(self, regex, positive_list, negative_list):
        # Assert all elements of positive_list match regex
        for (value_str, expected_match) in positive_list:
            match = regex.search(value_str)
            self.assertIsNotNone(match, "failed to match '%s'" % value_str)
            self.assertEqual(match.group(), expected_match)

        # Asesrt all elements of negative_list do not match regex
        for value_str in negative_list:
            match = regex.search(value_str)
            self.assertIsNone(match, "matched for '%s'" % value_str)


class WordTests_LinuxCNC(WordValueMatchTest):
    def test_float(self):
        self.regex_assertions(
            regex=dialects.linuxcnc.REGEX_FLOAT,
            positive_list=[
                ('1.2', '1.2'), ('1', '1'), ('200', '200'), ('0092', '0092'),
                ('1.', '1.'), ('.2', '.2'), ('-1.234', '-1.234'),
                ('-1.', '-1.'), ('-.289', '-.289'),
                (' 1.2', ' 1.2'), # leading whitespace
                # error cases (only detectable in gcode context)
                ('1.2e3', '1.2'),
            ],
            negative_list=['.']
        )

    def test_code(self):
        self.regex_assertions(
            regex=dialects.linuxcnc.REGEX_CODE,
            positive_list=[
                ('1.2', '1.2'), ('1', '1'), ('10', '10'),
                ('02', '02'), ('02.3', '02.3'),
                ('1.', '1'), ('03 ', '03'),
                (' 2', ' 2'), # leading whitespace
                # error cases (only detectable in gcode context)
                ('30.12', '30.1'),
            ],
            negative_list=['.2', '.']
        )
