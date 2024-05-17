
from loguru import logger
from .encoder._video_encoder import VideoEncoder
from .encoder._image_encoder import ImageEncoder

class EncoderFactory:
    @staticmethod
    def create_encoder(
        redis_data: dict,
        number_of_processors: int,
        processor_kwargs: dict,
    ):
        processor_type_map = {
            "M001": "Ray_DPIRProcessor",
            "M002": "Ray_DRURBPNSRF3Processor",
            "M003": "Ray_DRURBPNSRF5Processor"
        }
        processor_type = processor_type_map.get(redis_data.get("model"), "Ray_SleepAndPassProcessor")

        if redis_data.get("contentType") == "image":
            logger.debug("image encoder")
            return ImageEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
        else:
            logger.debug("video encoder")
            return VideoEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
        
        logger.debug("encoder init end")

# class Encoder:
#     def __init__(
#         self,
#         redis_data: dict,
#         number_of_processors: int,
#         processor_kwargs: dict,
#     ):
#         # processor_kwargs = {
#         #     "concurrency": 2,
#         #     "sleep_time": 0.1,
#         # } 
#         if redis_data.get("model") == "M001":
#             processor_type = "Ray_DPIRProcessor"
#         elif redis_data.get("model") == "M002":
#             processor_type = "Ray_DRURBPNSRF3Processor"
#         elif redis_data.get("model") == "M003":
#             processor_type = "Ray_DRURBPNSRF5Processor"
#         else:
#             processor_type = "Ray_SleepAndPassProcessor"
#             # raise "undefined model"
            
#         if redis_data.get("contentType") == "image":
#             logger.debug("image encoder")
#             self.encoder = ImageEncoder(
#                 processor_type=processor_type,  # processor_key,
#                 number_of_processors=number_of_processors,
#                 processor_kwargs=processor_kwargs
#             )
#         else:
#             logger.debug("video encoder")
#             self.encoder = VideoEncoder(
#                 processor_type=processor_type,  # processor_key,
#                 number_of_processors=number_of_processors,
#                 processor_kwargs=processor_kwargs
#             )
        
#         logger.debug("encoder init end")
        
#     async def run(self, *args, **kwargs) -> bool:
#         await self.encoder(*args, **kwargs)
        