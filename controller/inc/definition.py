from enum import Enum


class State(Enum):
    INIT = "init"
    ROAMING = "roaming"  # no trash detected
    DISCOVER_TRASH = "discovertrash"  # discover trash
    SHUTDONW = "shutdown"
