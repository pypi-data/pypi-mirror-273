import unittest
from esios.api_client import APIClient

class TestAPIClient(unittest.TestCase):

    def setUp(self):
        self.api_client = APIClient(api_key="test_key")

    def test_api_call(self):
        # This test is just a placeholder
        # You would mock requests and test _api_call
        pass

if __name__ == '__main__':
    unittest.main()
