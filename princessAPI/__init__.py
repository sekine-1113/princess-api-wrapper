# princessAPI
# Copyright 2023
# See LICEENSE for details.

__version__ = "2.0.0"
__license__ = "MIT"

from princessAPI.api import API
from princessAPI.consts import (
    Lang,
    IdolType,
    CardRarity,
    ExType,
    EventType,
)
from princessAPI.exceptions import (
    PrincessException,
    HTTPException,
    ServerError,
)
# Global
api = API()