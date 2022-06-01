import json
from log import logger
# Can be refactored to store cache in redis
def read_local_cache(cache_file: str = './cache.json') -> dict:
    """
    Check if local cache contains branches that need to be skipped
    """
    try:
        with open(cache_file) as file:
            cache = ''.join(file.readlines())
            if cache == '':
                logger.warning(f'{cache_file} is empty')
                return {}
            return json.loads(cache)
    except FileNotFoundError as err:
        logger.warning(err)
        return {}

def write_local_cache(
        cache_file: str = './cache.json', 
        cache_data: dict = {},
    ) -> None:
    """
    Write to local cache branches that need to be skipped
    """
    with open(cache_file, mode = 'w') as file:
        file.writelines(json.dumps(cache_data, indent=4))
