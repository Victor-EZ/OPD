import math
import unittest

def test(value, precision):
    sin_ = round(math.sin(value), precision)
    cos_ = round(math.cos(value), precision)
    tg_ = "Не вычисляется"
    ctg_ = tg_

    if cos_:
        tg_ = round(sin_ / cos_, precision)

    if sin_:
        ctg_ = round(cos_ / sin_, precision)

    return sin_, cos_, tg_, ctg_

class Test(unittest.TestCase):
    def test_0(self):
        self.assertEqual(test(0, 5), (0, 1, 0, "Не вычисляется"))

    def test_p2(self):
        self.assertEqual(test(math.pi / 2, 5), (1, 0, "Не вычисляется", 0))

    def test_p(self):
        self.assertEqual(test(math.pi, 5), (0, -1, 0, "Не вычисляется"))

if __name__ == '__main__':
    unittest.main()