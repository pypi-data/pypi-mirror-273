import unittest

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.completion import Completion
from openai.types.create_embedding_response import CreateEmbeddingResponse

from test_base_connection import TestServerClient

class OpenAiEndpointsTests(TestServerClient):
    
    openai_client = None
    chat_completions_engine_id = 'a8234b59-81ed-45e0-9378-2ccfb5c4d9f1'
    completions_engine_id = '4801422a-5c62-421e-a00c-05c6a9e15de8'
    embedding_engine_id = 'cb661f04-cb30-48fd-aafc-b4d422ce24e4'
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        if cls.openai_client is None:
            cls.openai_client = OpenAI(
                api_key="EMPTY",
                base_url=cls.server_client.get_openai_endpoint(),
                default_headers=cls.server_client.get_auth_headers()
            )
            
    def test_chat_completions_endpoint(self):
        response = self.openai_client.chat.completions.create(
            model=self.chat_completions_engine_id, # change the model name to a Model Engine ID
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )
        
        self.assertIsInstance(response, ChatCompletion)
        self.assertIsNotNone(response.choices[0].message.content)        
        self.assertIsInstance(response.choices[0].message.content, str)
        
    def test_completions_endpoints(self):
        response = self.openai_client.completions.create(
            model=self.completions_engine_id,
            prompt="Write a tagline for an ice cream shop."
        )
        
        self.assertIsInstance(response, Completion)
        self.assertIsNotNone(response.choices[0].text)        
        self.assertIsInstance(response.choices[0].text, str)
        
    def test_embeddings_endpoints(self):
        response = self.openai_client.embeddings.create(
            model=self.embedding_engine_id,
            input=["Your text string goes here"]
        )
        
        self.assertIsInstance(response, CreateEmbeddingResponse)
        self.assertIsNotNone(response.data[0].embedding)        
        self.assertGreater(len(response.data[0].embedding), 0)
        

if __name__ == '__main__':
    unittest.main()
