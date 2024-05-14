import os
import asyncio
from loguru import logger

class ImageEncoder:
    def __init__(
        self,
        processor_type: str,
        number_of_processors: int,
        processor_kwargs: dict,
    ):
        logger.debug("initiate image encoder")
        
    async def __call__(self, data) -> None:
        pass
        