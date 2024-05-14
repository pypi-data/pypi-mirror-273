import json
import logging

import redis

logger = logging.getLogger('uc_tools').addHandler(logging.NullHandler())


class Redis:
    def __init__(self, host, port, username='', password='', db=0):
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.client = self.connect()

    def connect(self):
        logger.info(f'Connecting to Redis server at ' f'{self.host}:{self.port}...')
        try:
            client = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db,
                username=self.username,
                password=self.password,
            )
            logger.info('Connected to Redis server.')
        except Exception as e:
            logger.exception(f'Failed to connect to Redis server: {e}')
            raise
        else:
            return client

    def get(self, key, decode_type=str):
        """
        Get value for key from Redis.
        """
        value = self.client.get(key)
        if value is None:
            return None
        if decode_type is bytes:
            return value
        try:
            return decode_type(value.decode('utf-8'))
        except (ValueError, AttributeError):
            logger.exception(f"Failed to decode value for key '{key}'")
            raise

    def set(self, key, value, ex=-1, encode_type=str):
        """
        Set value for key in Redis.

        Args:
            key: The key to set value for.
            value: The value to set.
            ex: The expire time in seconds.
            encode_type: The type to encode the value to.

        Returns:
            The result of the set operation.
        """
        logger.info(f"Setting value '{value}' for key '{key}' in Redis...")
        try:
            if encode_type is str:
                encoded_value = value.encode('utf-8')
            elif encode_type in {int, float, bool}:
                encoded_value = str(value).encode('utf-8')
            elif encode_type in {list, dict}:
                encoded_value = json.dumps(value)
            else:
                msg = 'Unsupported encode_type'
                raise ValueError(msg)

            result = self.client.set(
                key, encoded_value
            )  # WARNING: Удалил ex проблемы на винде
            logger.info(f'Set operation result: {result}')
        except Exception as e:
            logger.exception(
                f"Failed to set value '{value}' for key '{key}' " f'in Redis: {e}'
            )
            raise
        else:
            return result

    def delete(self, key):
        logger.info(f"Deleting key '{key}' from Redis...")
        try:
            result = self.client.delete(key)
            logger.info(f'Delete operation result: {result}')
            return result
        except Exception as e:
            logger.exception(f"Failed to delete key '{key}' from Redis: {e}")
            raise
