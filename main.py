from config.logging import logger as log
from config.db import AtlasConfig, AtlasCredentials, TypeOfAtlasCredentials

if __name__ == "__main__":
    log.info("Starting Stanlib application - @author Hi-kue")
    log.info("Connecting to Atlas MongoDB")
    db = AtlasConfig().mongo_connect()
    log.info(type(db))

