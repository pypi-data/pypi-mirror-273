# tests/test_version_util.py

import unittest
from lib_version_URLPhishing.version_util import VersionUtil

class TestVersionUtil(unittest.TestCase):

    def test_get_version(self):
        """Test that get_version returns the expected version."""
        expected_version = '2.0.0'  # Change this as needed
        result = VersionUtil.get_version()
        self.assertEqual(result, expected_version)

if __name__ == '__main__':
    unittest.main()
