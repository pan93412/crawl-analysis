from datetime import datetime
from typing import NotRequired, TypedDict
import bson


class FacebookPostModel(TypedDict):
    _id: NotRequired[bson.ObjectId]

    content: str

    likes_count: int
    url: str

    source: str  # page name, group name, etc.


class LineMessageModel(TypedDict):
    _id: NotRequired[bson.ObjectId]

    content: str
    post_at: datetime
    sender: str

    source: str  # chat name
