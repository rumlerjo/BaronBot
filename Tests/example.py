import unittest

class ExampleTest(unittest.TestCase):
    def test_example(self): #test_ required for function name
        self.assertEqual(3+3, 6)

if __name__ == "__main__":
    unittest.main()