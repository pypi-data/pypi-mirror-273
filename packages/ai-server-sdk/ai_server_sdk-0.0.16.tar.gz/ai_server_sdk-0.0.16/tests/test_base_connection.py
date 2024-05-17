import unittest
from ai_server import ServerClient

class TestServerClient(unittest.TestCase):
    
    server_client = None
    
    @classmethod
    def setUpClass(cls):
        # Create an instance of ServerClient for testing
        if cls.server_client is None:
            cls.server_client = TestServerClient.login_with_access_keys()
            
            
    @staticmethod
    def login_with_access_keys():
        from test_constants import ACCESS_KEY, SECRET_KEY, ENPOINT
        return ServerClient(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            base=ENPOINT
        )

if __name__ == '__main__':
    unittest.main()
