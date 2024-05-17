from typing import Optional
import logging
from ...server_resources.server_proxy import ServerProxy

logger: logging.Logger = logging.getLogger(__name__)

class StorageEngine(ServerProxy):

    def __init__(self, engine_id:str, insight_id: Optional[str] = None):
        super().__init__()
        
        self.engine_id = engine_id
        self.insight_id = insight_id
        
        logger.info("StorageEngine initialized with engine ID " + engine_id)

    def list(self, path:str, insight_id:Optional[str] = None):

        if insight_id is None:
            insight_id = self.insight_id

        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="list",
            method_args=[path],
            method_arg_types=["java.lang.String"],
        )

    def listDetails(self, path:str, insight_id:Optional[str] = None):
        if insight_id is None:
            insight_id = self.insight_id

        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="listDetails",
            method_args=[path],
            method_arg_types=["java.lang.String"],
        )

    def syncLocalToStorage(self, localPath:str, storagePath:str, insight_id: Optional[str] = None):
        if insight_id is None:
            insight_id = self.insight_id

        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="syncLocalToStorage",
            method_args=[localPath, storagePath],
            method_arg_types=["java.lang.String", "java.lang.String"],
        )

    def syncStorageToLocal(self, localPath:str, storagePath:str, insight_id:Optional[str] = None):
        if insight_id is None:
            insight_id = self.insight_id
            
        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="syncStorageToLocal",
            method_args=[storagePath, localPath],
            method_arg_types=["java.lang.String", "java.lang.String"],
        )

    def copyToLocal(self, storageFilePath:str, localFolderPath:str, insight_id:Optional[str] = None):
        if insight_id is None:
            insight_id = self.insight_id
            
        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="copyToLocal",
            method_args=[storageFilePath, localFolderPath],
            method_arg_types=["java.lang.String", "java.lang.String"],
        )

    def deleteFromStorage(self, storagePath, insight_id=None):
        if insight_id is None:
            insight_id = self.insight_id

        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="deleteFromStorage",
            method_args=[storagePath],
            method_arg_types=["java.lang.String"],
        )

    def deleteFromStorage(
        self, storagePath:str, leaveFolderStructure:Optional[bool] = False, insight_id:Optional[str] = None
    ):
        if insight_id is None:
            insight_id = self.insight_id
            
        return super().call(
            engine_type="Storage",
            engine_id=self.engine_id,
            insight_id=insight_id,
            method_name="deleteFromStorage",
            method_args=[storagePath, leaveFolderStructure],
            method_arg_types=["java.lang.String", "java.lang.Boolean"],
        )
