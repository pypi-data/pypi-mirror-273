import os

def delete_temp_files(
    redis_data: dict
) -> None:
    # best quality file
    path = "/app/tmp/{}_max.{}".format(
        redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
    
    # dummy file
    path = "/app/tmp/{}_dummy.{}".format(
        redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
        
    # two pass log file
    path = "/app/tmp/{}-0.log".format(
        redis_data["fileKey"]
    )
    if os.path.exists(path):
        os.remove(path)
        
    # two pass mbtree file
    path = "/app/tmp/{}-0.log.mbtree".format(
        redis_data["fileKey"]
    )
    if os.path.exists(path):
        os.remove(path)
        
    # audio file
    path = "/app/tmp/{}_audio.{}".format(
        redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)