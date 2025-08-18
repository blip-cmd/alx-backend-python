"""
Basic tests for the messaging app - Non-Django tests
"""
import unittest


class BasicTest(unittest.TestCase):
    """Basic test to verify test framework works"""
    
    def test_basic_functionality(self):
        """Test that the test framework is working"""
        self.assertTrue(True)
        
    def test_math_operations(self):
        """Test basic math operations"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(5 * 3, 15)
        
    def test_string_operations(self):
        """Test string operations"""
        test_string = "Hello World"
        self.assertEqual(len(test_string), 11)
        self.assertTrue(test_string.startswith("Hello"))
        self.assertTrue(test_string.endswith("World"))


if __name__ == '__main__':
    unittest.main()