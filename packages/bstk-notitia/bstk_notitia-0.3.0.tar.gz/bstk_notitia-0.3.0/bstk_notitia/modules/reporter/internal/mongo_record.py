from __future__ import annotations
from types import NoneType
import typing
from bstk_notitia.lib.abc.reporter import ReporterABC

if typing.TYPE_CHECKING:
    from modules.driver.mongodb import NotitiaModule as MongoDBDriver, DriverABC
    from pymongo.results import (
        UpdateResult,
        InsertManyResult,
        InsertOneResult,
        DeleteResult,
    )
    from asyncio import Future

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
    },
}


class NotitiaModule(ReporterABC):
    name = "Internal MongoDB Record Reporter"
    key = "internal/mongodb_record"

    if typing.TYPE_CHECKING:
        driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    async def receive(
        self,
        action: str,
        data: typing.Union[typing.List[typing.Dict], typing.Dict],
        record: typing.Optional[typing.Dict] = None,
        constraints: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        brief = None
        if action == "update":
            if not record or not record.get("_id"):
                return False

            stream = self.driver["mongodb"].get_collection().update_one
            if not constraints:
                constraints = {"_id": record["_id"]}
            else:
                constraints["_id"] = record["_id"]

            if not self._has_update_operators(data):
                data = {"$set": data}

            stream_params = {"filter": constraints, "update": data}

        if action == "insert":
            if isinstance(data, list):
                stream = self.driver["mongodb"].get_collection().insert_many
                stream_params = {"documents": data}
            else:
                stream = self.driver["mongodb"].get_collection().insert_one
                stream_params = {"document": data}

        if not stream:
            return False

        brief = stream(**stream_params)

        if not brief:
            return False

        res = await self.publish(brief)
        return res

    def _has_update_operators(self, data: typing.Dict[str, any]) -> bool:
        _k = list(data)[0]
        if _k[0:1] == "$":
            return True

        return False

    async def publish(self, brief: Future) -> typing.Any:
        result: typing.Union[
            UpdateResult, InsertManyResult, InsertOneResult, DeleteResult
        ] = await brief

        if not result.acknowledged:
            return False

        if hasattr(result, "matched_count") and not result.matched_count:
            return NoneType

        if hasattr(result, "inserted_ids") and result.inserted_ids:
            return result.inserted_ids

        if hasattr(result, "inserted_id") and result.inserted_id:
            return result.inserted_id

        if hasattr(result, "modified_count") and result.modified_count:
            return result.modified_count

        if hasattr(result, "deleted_count") and result.deleted_count:
            return result.deleted_count
