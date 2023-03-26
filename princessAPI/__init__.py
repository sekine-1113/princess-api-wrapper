__version__ = "2.0.0"

import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from princessAPI.api import API
from princessAPI.consts import (
    Lang,
    IdolType,
    CardRarity,
    ExType,
    EventType,
)
