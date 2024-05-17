from typing import (
    List, 
    Dict,
    Optional
)
import json

from ...server_resources.server_proxy import ServerProxy

class VectorEngine(ServerProxy):
    '''Python class to interact with Vector Database Engines defined in CFG AI'''
    
    engine_type = 'VECTOR'
    
    def __init__(
        self,
        engine_id:str, 
        insight_id:Optional[str] = None,
    ):
        super().__init__()
        self.engine_id = engine_id
        self.insight_id = insight_id
        
    def addDocument(
        self,
        file_paths:List[str],
        param_dict:Optional[Dict] = {},
        insight_id:Optional[str] = None,
    ) -> None:
        '''
        This method is used to add documents to a vector database. The engine itself will determine how the the documents are 
        processed and the embeddings are created.
        
        Args:
            file_paths (`List[str]`): List of local files paths to push to the server and index.
            param_dict (`Optional[Dict]`): Additional parameters the engine might need to process the documents.
            insight_id (`Optional[str]`): The insight ID to upload the documents to and process the request. Default is to use the clients current insight.
            
        Returns:
            `None`
        '''
        if insight_id is None:
            if self.insight_id is None:
                insight_id = self.insight_id
            else:
                insight_id = self.server.cur_insight
                      
        assert self.server != None
        insight_files = self.server.upload_files(
            files = file_paths, 
            insight_id = insight_id, 
        )
        
        pixel = "CreateEmbeddingsFromDocuments (engine = \"" + self.engine_id + "\", filePaths = "+json.dumps(insight_files)
        
        if len(param_dict) != 0:
            pixel += ", paramValues = " + json.dumps(param_dict)
        
        pixel += ");"
        
        output_payload_message = self.server.run_pixel(
            payload = pixel, 
            insight_id = insight_id,
            full_response = True
        )
        
        if (output_payload_message['pixelReturn'][0]['operationType'] == ['ERROR']):
            raise RuntimeError(output_payload_message['pixelReturn'][0]['output'])
        
        # output_payload_message['pixelReturn'][0]['output']
        
            
    def removeDocument(
        self,
        file_names:List[str],
        param_dict:Optional[Dict] = {},
        insight_id:Optional[str] = None,
    ):
        '''
        Remove document(s) and their embeddings from a vector database.
        
        Args:
            file_names (`List[str]`): List of files names that you want to remove from the db. The files should exist in the vector database.
            param_dict (`Optional[Dict]`): Additional parameters the engine might need to remove the documents.
            insight_id (`Optional[str]`): The insight ID to upload the documents to and process the request. Default is to use the clients current insight.
            
        Returns:
            `None`
        '''
        
        if insight_id == None:
            insight_id = self.insight_id
        
        param_dict['insight'] = insight_id
        
        return super().call(
            engine_type = VectorEngine.engine_type, 
            engine_id = self.engine_id, 
            method_name = 'removeDocument', 
            method_args=[file_names, param_dict],
            method_arg_types=['java.util.List', 'java.util.Map'],
            insight_id = insight_id
        )
    
    def nearestNeighbor(
        self,
        search_statement:str,
        limit:Optional[int] = 5,
        param_dict:Optional[Dict] = {},
        insight_id:Optional[str] = None,
    ) -> List[Dict]:
        '''
        Perform a nearest neighbor or semantic search against a vector database. The searchStatement will be 
        converted to a vector using the same embedding model utilized to create the document(s) embeddings.
        
        
        Args:
            search_statement (`str`): The statement to search for semantic matches in the vector database
            limit (`Optional[int]`): The amount of top matches to return
            param_dict (`Optional[Dict]`): Additional parameters the engine might need to remove the documents.
            insight_id (`Optional[str]`): The insight ID to upload the documents to and process the request. Default is to use the clients current insight.
            
        Returns:
            `List[Dict]`: A list of dictionaries that contain the top semantic matches against the search statement
        '''
               
        if insight_id is None:
            if self.insight_id is None:
                insight_id = self.insight_id
            else:
                insight_id = self.server.cur_insight
    
        
        pixel = f"VectorDatabaseQuery(engine = \"{self.engine_id}\", command = [\"<e>{search_statement}</e>\"], limit = {limit}"
        
        if len(param_dict) != 0:
            pixel += ", paramValues = " + json.dumps(param_dict)
        
        pixel += ");"
        
        output_payload_message = self.server.run_pixel(
            payload = pixel, 
            insight_id = insight_id,
            full_response = True
        )
        
        if (output_payload_message['pixelReturn'][0]['operationType'] == ['ERROR']):
            raise RuntimeError(output_payload_message['pixelReturn'][0]['output'])
        
        return output_payload_message['pixelReturn'][0]['output']
    
    def listDocuments(
        self,
        param_dict:Optional[Dict] = {},
        insight_id:Optional[str] = None,
    ) -> List[Dict]:
        '''
        List the set of documents a vector database is made from. At a minimum the file names should be returned but 
        the file size and last modified date are also options.
        
        Args:
            param_dict (`Optional[Dict]`): Additional parameters the engine might need to remove the documents.
            insight_id (`Optional[str]`): The insight ID to upload the documents to and process the request. Default is to use the clients current insight.
            
        Returns:
            `List[Dict]`: A list of dictionaries that contain file information
        '''
        if insight_id == None:
            insight_id = self.insight_id
        
        return super().call(
            engine_type = VectorEngine.engine_type, 
            engine_id = self.engine_id, 
            method_name = 'listDocuments', 
            method_args=[param_dict],
            method_arg_types=['java.util.Map'],
            insight_id = insight_id
        )
