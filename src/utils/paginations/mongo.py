"""
Mongo DB pagination
"""

import bson

from typing import Any
from typing import List
from typing import Dict
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection


class MongoPaginator:
    """
    Implements pagination for MongoDB collections using a cursor-based approach.

    Attributes:
        collection (AsyncIOMotorCollection): The MongoDB collection to paginate.
        query (Dict[str, Any]): The query filter for the collection.
        limit (int): The maximum number of items per page.
        cursor (Optional[str]): The starting point for pagination, represented as an ObjectId.
        next_cursor (Optional[str]): The cursor for the next page of results.
        previous_cursor (Optional[str]): The cursor for the previous page of results.
        sort (int): Sorting order for the '_id' field (-1 for descending, 1 for ascending).
    """

    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        query: Dict[str, Any],
        limit: int,
        cursor: Optional[str] = None
    ):
        """
        Initialize the paginator with the collection, query, and pagination settings.

        Args:
            collection (AsyncIOMotorCollection): The MongoDB collection to paginate.
            query (Dict[str, Any]): The query filter for the collection.
            limit (int): The maximum number of items per page.
            cursor (Optional[str], optional): Starting point for pagination, as an ObjectId string.
        """
        self.collection = collection
        self.query = query
        self.limit = limit
        self.cursor = bson.ObjectId(cursor) if cursor else None
        self.next_cursor: Optional[str] = None
        self.previous_cursor: Optional[str] = None
        self.sort = -1

    async def has_next(self, last_item: bson.ObjectId) -> bool:
        """
        Check if there is a next page of results.

        Args:
            last_item (bson.ObjectId): The ObjectId of the last item in the current page.

        Returns:
            bool: True if a next page exists, False otherwise.
        """
        result = await self.collection.find_one({"_id": {"$lt": last_item}})
        return True if result else False

    async def has_previous(self, first_item: bson.ObjectId) -> bool:
        """
        Check if there is a previous page of results.

        Args:
            first_item (bson.ObjectId): The ObjectId of the first item in the current page.

        Returns:
            bool: True if a previous page exists, False otherwise.
        """
        result = await self.collection.find_one({"_id": {"$gt": first_item}})
        return True if result else False

    async def get_page(self, forward: bool = True) -> List[Dict[str, Any]]:
        """
        Retrieve a page of results based on the current cursor and direction.

        Args:
            forward (bool, optional): Direction of pagination. Defaults to True (next page).

        Returns:
            List[Dict[str, Any]]: A list of documents for the current page.
        """
        if self.cursor:
            if forward:
                self.query['_id'] = {'$lt': self.cursor}
            else:
                self.query['_id'] = {'$gt': self.cursor}

        cursor = (
            self.collection
            .find(self.query)
            .sort('_id', self.sort)
            .limit(self.limit)
        )

        results = await cursor.to_list(length=None)

        if results:
            if await self.has_previous(results[0]['_id']):
                self.previous_cursor = str(results[0]['_id'])
            else:
                self.previous_cursor = None

            if len(results) < self.limit:
                self.next_cursor = None
            else:
                if await self.has_next(results[-1]['_id']):
                    self.next_cursor = str(results[-1]['_id'])
                else:
                    self.next_cursor = None
        else:
            self.next_cursor = None
            self.previous_cursor = None

        return results
