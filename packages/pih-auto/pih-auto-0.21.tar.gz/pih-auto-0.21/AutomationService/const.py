import ipih

from enum import IntEnum, auto
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "Automation"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.21"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Automation service",
    host=HOST.NAME,
    use_standalone=True,
    standalone_name="auto",
    version=VERSION,
)

UNISEND_API_URL: str = "https://api.unisender.com/ru/api/subscribe"


class ProblemState(IntEnum):
    AT_FIX = auto()
    WAIT_FOR_FIX_RESULT = auto()
    NOT_FIXED = auto()
    FIXED = auto()
