from . import BaseClient

from .utilities.decorators import validate_document_type

class RHClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        
    @validate_document_type
    async def index_document(self, document_content: str, is_cv: bool=False, is_job: bool=False) -> None:
        if is_cv:
            pass
        if is_job:
            pass
    
    @validate_document_type
    async def index_file(self, file_path: str, is_cv: bool=False, is_job: bool=False) -> None:
        # Read the file content
        if is_cv:
            pass
        if is_job:
            pass
    
if __name__ == '__main__':
    pass