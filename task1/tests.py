import unittest
from solution import sum_two


class TestTimeService(unittest.TestCase):

    def test_sum_ok(self):
        values = (
            (1, 2),
            (3, 4),
            (3, 6),
            (6, 7),
            (8, 9),
            (9, 1),
            (6, 5),
        )
        for a, b in values:
            with self.subTest():
                self.assertEqual(sum_two(a, b), a + b)

    def test_sum_error(self):
        values = (
            (1, 2.4),
            (1.1, 5.1),
            (5.3, 6),
            ('test', 7),
            ('test', 'test'),
            (True, 1),
            (True, False),
        )
        for a, b in values:
            with self.subTest():
                with self.assertRaises(TypeError):
                    sum_two(a, b)


unittest.main()
