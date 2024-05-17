import asyncio

from .rh import RHClient
from .utilities.log import logger

async def main():
    client = RHClient('goo_12493RUIJF498RFJ4')
    await client.hello()
    
if __name__ == '__main__':
    asyncio.run(main())