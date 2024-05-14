import re
from enum import Enum

# from .models import (
#     BudgetTypeEnum,
#     TravelPartyCompositionEnum,
# )

DEFAULT_LANGUAGE = "es"

MODEL_TABLE = "model"

UID_TYPE = str

MONOTONIC_KEY = 'wave__'
MONOTONIC_SINCE = 'since__'
MONOTONIC_SINCE_KEY = 'since_key__'
MONOTONIC_SINCE_VALUE = 'since_value__'
ALT_KEY = 'id__'
REG_PRIVATE_KEY = r".*__$"


def filter_private(data):
    return {
        key: value
        for key, value in data.items()
        if not re.match(REG_PRIVATE_KEY, key)
    }


# ----------------------------------------------------------
# enumerate helpers
# ----------------------------------------------------------
