import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoConnector:
    def __init__(self) -> None:
        load_dotenv()
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster_url = os.getenv("MONGODB_CLUSTER_URL")
        app_name = os.getenv("MONGODB_APP_NAME")

        uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?appName={app_name}"

        print(uri)

        self.client = MongoClient(uri)
        self.database = self.client.get_database("popl")

    def get_collection(self, collection_name) -> Collection:
        return self.database.get_collection(collection_name)
