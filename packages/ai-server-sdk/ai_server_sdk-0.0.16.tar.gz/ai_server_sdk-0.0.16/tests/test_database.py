import unittest
import pandas as pd

from test_base_connection import TestServerClient
from ai_server import DatabaseEngine

class DatabaseTests(TestServerClient):
    
    database_engine_id = "995cf169-6b44-4a42-b75c-af12f9f45c36"
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_engine = DatabaseEngine(
            engine_id = cls.database_engine_id, 
        )  
        
    def test_db_query(self):
        db_pandas = self.db_engine.execQuery('select * from diabetes')
        
        # Assert that the response is a dictionary with specific keys
        self.assertIsInstance(db_pandas, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
