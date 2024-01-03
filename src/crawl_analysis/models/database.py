import os
import pymongo
from pymongo.collection import Collection
from torch import unique

from models.post import FacebookPostModel, LineMessageModel

class TypedDatabase:
    def __init__(self, uri: str | None = None, db = "crawl_analysis"):
        if uri is None:
            uri = os.environ["MONGODB_URI"]

        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db]

    def facebook_post_model(self) -> Collection[FacebookPostModel]:
        col_name = "facebook_posts"

        if col_name not in self.db.list_collection_names():
            post_collection: Collection[FacebookPostModel] = self.db.create_collection(col_name)
            post_collection.create_index("url", unique=True)

        return self.db[col_name]

    def line_message_model(self) -> Collection[LineMessageModel]:
        col_name = "line_messages"
        return self.db[col_name]
