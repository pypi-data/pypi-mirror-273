from dataclasses import dataclass, field
import decimal
import typing
from bstk_notitia.lib.abc.driver import DriverABC

import bson
from bson import codec_options
import motor.motor_asyncio
import motor.docstrings
import pymongo.errors

from datetime import datetime, date, time
from enum import Enum


def _bson_encode(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, decimal.Decimal):
        return bson.Decimal128(value)
    if (
        isinstance(value, object)
        and hasattr(value, "_to_json")
        and callable(value._to_json)
    ):
        return value._to_json()

    if isinstance(value, date):
        return datetime.combine(value, time.min)

    return None


class DecimalCodec(codec_options.TypeCodec):
    python_type = decimal.Decimal  # the Python type acted upon by this type codec
    bson_type = bson.Decimal128  # the BSON type acted upon by this type codec

    def transform_python(self, value: decimal.Decimal):
        """Function that transforms a custom type value into a type
        that BSON can encode. We use a precision of 30 to avoid overflows
        and other weird shit that happens during floatfuckery"""
        return bson.Decimal128(decimal.Context(prec=30).create_decimal(value))

    def transform_bson(self, value: bson.Decimal128):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return value.to_decimal()


mongod_params = {
    "connectTimeoutMS": "2000",
    "heartbeatFrequencyMS": "1000",
    "serverSelectionTimeoutMS": "5000",
    "tz_aware": True,
    "uuidRepresentation": "pythonLegacy",
    "type_registry": codec_options.TypeRegistry(
        [DecimalCodec()], fallback_encoder=_bson_encode
    ),
}


@dataclass
class NotitiaModule(DriverABC):
    """
    The mongodb driver module provides a thin facade around mongo_motor.

    In general, all modules can use different collections and databases,
    but the DSN is managed per-department.

    Implementors can be specific, targeting databases and collections,
    or implicit, using the parameters provided by the investigator during
    startup.

    Regardless of which implementation is used, the only interface provided
    by this module that wouldn't normally be available is the `watch` command
    which provides a functional wrapper around a mongo change stream.
    """

    name = "MongoDB (Motor) driver"
    key = "driver/mongodb"

    dsn: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    database: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    collection: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    connections: typing.Dict[typing.AnyStr, motor.motor_asyncio.AsyncIOMotorClient] = (
        field(init=False, default_factory=dict)
    )

    # Notitia
    def connect(
        self, dsn: typing.Optional[typing.AnyStr] = None
    ) -> motor.motor_asyncio.AsyncIOMotorClient:
        if not dsn and self.dsn:
            dsn = self.dsn

        if dsn not in self.connections:
            self.connections[dsn] = motor.motor_asyncio.AsyncIOMotorClient(
                dsn, **mongod_params
            )

        return self.connections[dsn]

    def disconnect(self, dsn: typing.Optional[str] = None):
        if dsn:
            if dsn not in self.connections:
                return

            self.connections[dsn].close()
            return

        for _conn in self.connections.values():
            _conn.close()

    # Native
    def get_db(
        self,
        name: typing.Optional[str] = None,
        client: typing.Optional[motor.motor_asyncio.AsyncIOMotorClient] = None,
    ) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        if client is None and self.dsn:
            client = self.connect(self.dsn)

        if not name and self.database:
            name = self.database

        return client[name]

    def get_collection(
        self,
        name: typing.Optional[str] = None,
        db: typing.Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None,
    ) -> motor.motor_asyncio.AsyncIOMotorCollection:
        if db is None and self.dsn and self.database:
            db = self.get_db()

        if not name and self.collection:
            name = self.collection

        return db[name]

    async def watch(
        self,
        pipeline: typing.List,
        collection: typing.Optional[motor.motor_asyncio.AsyncIOMotorCollection] = None,
        resume_token: typing.Optional[typing.AnyStr] = None,
        **kwargs,
    ) -> typing.AsyncGenerator[typing.Tuple[typing.AnyStr, typing.Dict], None]:
        if collection is None:
            if self.collection:
                collection = self.get_collection(self.collection)

        try:
            async with collection.watch(
                pipeline, resume_after=resume_token, **kwargs
            ) as stream:
                async for change in stream:
                    resume_token = stream.resume_token
                    yield (resume_token, change)
        except pymongo.errors.PyMongoError as ex:
            # The ChangeStream encountered an unrecoverable error or the
            # resume attempt failed to recreate the cursor.
            if resume_token is None:
                # There is no usable resume token because there was a
                # failure during ChangeStream initialization.
                print(ex)
                return

            # Use the interrupted ChangeStream's resume token to
            # create a new ChangeStream. The new stream will
            # continue from the last seen insert change without
            # missing any events.
            async with collection.watch(
                pipeline, resume_after=resume_token, **kwargs
            ) as stream:
                async for change in stream:
                    resume_token = stream.resume_token
                    yield (resume_token, change)
