from .utilities.log import logger

class BaseClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        
    def __repr__(self):
        return f'<{self.__class__.__name__} api_key={self._api_key}>'
    
    def __str__(self):
        return self.__repr__()
    
    async def hello(self):
        logger.info('Hello, World!')