import unittest
from typing import Generator
from ai_server import ModelEngine

from test_base_connection import TestServerClient

class ModelTests(TestServerClient):
    
    ask_engine_id = 'a8234b59-81ed-45e0-9378-2ccfb5c4d9f1'
    embedding_engine_id = 'cb661f04-cb30-48fd-aafc-b4d422ce24e4'
    
    def test_model_ask(self):
        model = ModelEngine(
            engine_id = self.ask_engine_id, 
        )

        model_response_list = model.ask(question = 'what is the capital of france ey?')

        # Assert that the response is a dictionary with specific keys
        self.assertIsInstance(model_response_list, list)
        
        model_response = model_response_list[0]
        self.assertIsInstance(model_response, dict)
        
        self.assertCountEqual(model_response.keys(), ['response', 'numberOfTokensInPrompt', 'numberOfTokensInResponse' , 'messageId', 'roomId'])
        
    def test_model_ask_with_stream(self):
        
        model = ModelEngine(
            engine_id = self.ask_engine_id, 
        )

        model_response_stream = model.stream_ask(question = 'what is the capital of france ey?')

        self.assertIsInstance(model_response_stream, Generator)
        
    def test_model_embeddings(self):
        model = ModelEngine(
            engine_id = self.embedding_engine_id, 
        )

        model_response_list = model.embeddings(strings_to_embed = ['what is the capital of france ey?'])

        # Assert that the response is a dictionary with specific keys
        self.assertIsInstance(model_response_list, list)
        
        model_response = model_response_list[0]
        self.assertIsInstance(model_response, dict)
        
        self.assertCountEqual(model_response.keys(), ['response', 'numberOfTokensInPrompt', 'numberOfTokensInResponse'])
        

if __name__ == '__main__':
    #python test_model.py -v -m "access_key=my_access_key secret_key=my_secret_key base=http://example.com/api"

    unittest.main()
