from agora_config import config
from agora_logging import logger
import redis

class RedisClientSingleton(redis.Redis): 
    '''
    Basic wrapper to unify how the connection to Redis is declared/configured.
    '''
    _instance: redis.Redis = None
    """
    Connects to the Redis Server from Agora Core    
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):        
        self.connect_attempted = False
        pass   
      
    def connect(self):
        '''
        Connects to Redis
        
        Use 'AEA2:RedisClient:Server' to set the server address (default = 'redis').
        Use 'AEA2:RedisClient:Port' to set the port (default = 6379).
        
        When running on gateway, the default values are appropriate.
        '''
        server = config["AEA2:RedisClient:Server"]
        if server == "":
            server = "localhost"

        port = config["AEA2:RedisClient:Port"]
        if port == "":
            port = "6379"  

        logger.info(f"redis_client connecting to '{server}:{port}'")
        self.connect_attempted = True
        super().__init__(host=server, port=port, decode_responses=True, socket_keepalive=True)   
        
        if self.is_connected():
            logger.info("redis_client connected")
      
    def is_connected(self):
        '''Returns 'True' if connected to Redis.'''
        try:             
            if self.ping():      
                return True
        except Exception as e:
            logger.error("Failed to ping redis.")
        return False

redis = RedisClientSingleton()
