import unittest
from jasyllablesep import parse

class TestSyllableSeparator(unittest.TestCase):
    def test_parse(self):
        cases = [
            ("シンシュンシャンソンショー", ['シン', 'シュン', 'シャン', 'ソン', 'ショー']),
            ("トーキョートッキョキョカキョク", ['トー', 'キョー', 'トッ', 'キョ', 'キョ', 'カ', 'キョ', 'ク']),
            ("アウトバーン", ['ア', 'ウ', 'ト', 'バーン']),
            ("ガッキュウホウカイ", ['ガッ', 'キュ', 'ウ', 'ホ', 'ウ', 'カ', 'イ'])
        ]
        
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(parse(text), expected)

if __name__ == '__main__':
    unittest.main()
