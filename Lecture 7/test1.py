import unittest

from prime import is_prime

class Tests(unittest.TestCase):
    def test1(self):
        """Check that 1 is not prime."""
        self.assertFalse(is_prime(1))
    
    def test2(self):
        """Check that 4 is not prime."""
        self.assertFalse(is_prime(4))
    
    def test3(self):
        """Check that 7 is prime."""
        self.assertTrue(is_prime(7))
    
    def test4(self):
        """Check the 25 is not prime."""
        self.assertFalse(is_prime(25))

if __name__ == "__main__":
    unittest.main()