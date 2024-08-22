from curl_cffi.requests import AsyncSession
from config.db import AtlasConfig, AtlasCredentials, TypeOfAtlasCredentials
from config.logging import logger as log
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import csv
import os

load_dotenv(".env")

with open("data/urls.csv", "r") as file:
    reader = csv.reader(file)
    urls = [url[0] for url in reader]


async def run():
    async with AsyncSession() as session:
        proxy = os.environ["PROXY"]
        if proxy is not None:
            session.proxies = {
                "http": proxy,
                "https": proxy
            }
        else:
            log.logger.warning("No PROXY .env variable found!")

        tasks = []

        for url in urls:
            task = session.get(url)
            tasks.append(task)

        response = await asyncio.gather(*tasks)

    return response


if __name__ == "__main__":
    data = asyncio.run(run())
    failed = []
    results = []

    for response in data:
        if response.status_code != 200:
            log.logger.warning(f"Failed on {response.url} with status {response.status_code}")
            failed.append(response.url)

        else:
            results.append({
                "url": response.url,
                "status": response.status_code,
                "content": response.text,
                "date": datetime.now(),
            })

    client = AtlasConfig().mongo_connect()
    db = client[AtlasCredentials.MONGO_DB]
    collection = db[AtlasCredentials.MONGO_COLLECTION]

    if len(results) > 0:
        insert_data = collection.insert_many(results)
        log.logger.info(f"Inserted {len(insert_data.inserted_ids)} documents successfully")