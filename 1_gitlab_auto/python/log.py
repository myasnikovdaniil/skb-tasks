import logging

# Logging setting
logging.basicConfig(format = '%(asctime)s %(levelname)s %(message)s',
                    # filename = 'script.log', 
                    encoding = 'utf-8', 
                    level = logging.DEBUG
                )

logger = logging.getLogger('my_logger')