from ._server import (
    FakeServer,
    FakeRedis,
    FakeStrictRedis,
    FakeConnection,
)
from .aioredis import (
    FakeRedis as FakeAsyncRedis,
    FakeConnection as FakeAsyncConnection,
)

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore
__version__ = metadata.version("fakeredis")
__author__ = "Daniel Moran"
__maintainer__ = "Daniel Moran"
__email__ = "daniel@moransoftware.ca"
__license__ = "BSD-3-Clause"
__url__ = "https://github.com/cunla/fakeredis"
__bugtrack_url__ = "https://github.com/cunla/fakeredis/issues"

__all__ = [
    "FakeServer",
    "FakeRedis",
    "FakeStrictRedis",
    "FakeConnection",
    "FakeAsyncRedis",
    "FakeAsyncConnection",
]
