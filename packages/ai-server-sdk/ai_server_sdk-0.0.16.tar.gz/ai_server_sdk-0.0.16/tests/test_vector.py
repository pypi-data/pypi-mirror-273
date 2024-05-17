import unittest
import os

from test_base_connection import TestServerClient
from ai_server import VectorEngine

class VectorTests(TestServerClient):
    
    vector_engine_id = "e6c720bb-eeeb-428a-8ae5-579a1025a487"
    vector_engine = None
    test_files = None
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vector_engine = VectorEngine(
            engine_id = cls.vector_engine_id, 
        )
        
        if cls.test_files is None:
            CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            TEST_FILE_DIR = os.path.join(CURRENT_DIR, "test_files")
            # List files with full paths
            TEST_FILES = [os.path.join(TEST_FILE_DIR, file) for file in os.listdir(TEST_FILE_DIR)]
            cls.test_files = TEST_FILES
        
    def test_vector_search(self):
        vector_search = self.vector_engine.nearestNeighbor(
            search_statement = 'How did the WHO improve access to oxygen supplies?', 
            limit = 5
        )
        
        # Assert that the response is a dictionary with specific keys
        self.assertIsInstance(vector_search, list)
        
        top_match = vector_search[0]
        self.assertIsInstance(top_match, dict)
        
        self.assertCountEqual(top_match.keys(), ['Score', 'Source', 'Modality' , 'Divider', 'Part', 'Tokens', 'Content'])
        
    def test_list_documetns(self):

        document_info_list = self.vector_engine.listDocuments()[0]

        self.assertIsInstance(document_info_list, list)
        
        if len(document_info_list) > 0:   
            document_info = document_info_list[0]
            self.assertIsInstance(document_info, dict)
            self.assertIn('fileName', document_info)
              
    def test_document_add_and_remove(self):
        from pathlib import Path
        
        self.vector_engine.addDocument(
            file_paths=self.test_files
        )

        file_names = [Path(file).name for file in self.test_files]
        
        self.vector_engine.removeDocument(file_names=file_names)

if __name__ == '__main__':
    unittest.main()
