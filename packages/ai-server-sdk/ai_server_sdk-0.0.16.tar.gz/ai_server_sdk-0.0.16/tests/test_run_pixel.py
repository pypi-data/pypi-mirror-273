import unittest
from test_base_connection import TestServerClient

class TestRunPixel(TestServerClient):
    
    def test_server_connection(self):
        # Mock response from the server
        expected_response = 2

        # Test the server connection
        response = self.server_client.run_pixel('1+1')  # Replace some_method with the actual method you're testing
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()
