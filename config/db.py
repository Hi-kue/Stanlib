import os
import time

from pymongo.mongo_client import MongoClient
from pymongo.errors import ConfigurationError
from config.logging import logger as log
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(".env")


@dataclass
class AtlasCredentials:
    MONGO_URI: str = os.environ["MONGO_URI"]
    MONGO_PORT: int = os.environ["MONGO_PORT"]
    MONGO_DB: str = os.environ["MONGO_DB"]
    MONGO_COLLECTION: str = os.environ["MONGO_COLLECTION"]
    MONGO_USER: str = os.environ["MONGO_USER"]
    MONGO_PASS: str = os.environ["MONGO_PASS"]


@dataclass
class TypeOfAtlasCredentials:
    MONGO_URI = type(AtlasCredentials.MONGO_URI)
    MONGO_PORT = type(AtlasCredentials.MONGO_PORT)
    MONGO_DB = type(AtlasCredentials.MONGO_DB)
    MONGO_COLLECTION = type(AtlasCredentials.MONGO_COLLECTION)
    MONGO_USER = type(AtlasCredentials.MONGO_USER)
    MONGO_PASS = type(AtlasCredentials.MONGO_PASS)


class AtlasConfig:
    def __init__(self, credentials: AtlasCredentials = AtlasCredentials()):
        self.credentials = credentials
        self.database = self.mongo_connect()

    def __check_credentials(self):
        if self.credentials.MONGO_URI is None:
            log.info("MONGO_URI is not set in .env file.")
            raise ConfigurationError("MONGO_URI is not set in .env file.")

        if self.credentials.MONGO_DB is None:
            log.info("MONGO_DB is not set in .env file.")
            raise ConfigurationError("MONGO_DB is not set in .env file.")

        if self.credentials.MONGO_USER is None:
            log.info("MONGO_USER is not set in .env file.")
            raise ConfigurationError("MONGO_USER is not set in .env file.")

        if self.credentials.MONGO_PASS is None:
            log.info("MONGO_PASS is not set in .env file.")
            raise ConfigurationError("MONGO_PASS is not set in .env file.")

    def mongo_connect(self):
        self.__check_credentials()

        start_time = time.time()
        client = MongoClient(self.credentials.MONGO_URI)

        try:
            log.info(f"Connection to Cluster {self.credentials.MONGO_DB} as {self.credentials.MONGO_USER}.")

            # Check credentials of MongoDB connection
            log.info(f"Credentials: {client.server_info()}")
            log.info(f"Connected to MongoDB cluster {AtlasCredentials.MONGO_COLLECTION} in {time.time() - start_time} seconds") # noqa

        except Exception as e:
            log.error(f"Error connecting to MongoDB: {e}")

        return client[self.credentials.MONGO_DB]

    def get_collection(self, collection_name: str):
        collection = self.database[collection_name]

        if collection is None:
            log.info(f"Collection {collection_name} not found.")
            raise ConfigurationError(f"Collection {collection_name} not found.")
