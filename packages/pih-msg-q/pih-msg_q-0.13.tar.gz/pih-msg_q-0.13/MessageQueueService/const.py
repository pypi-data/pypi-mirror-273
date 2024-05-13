import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

NAME: str = "MessageQueue"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.13"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Message queue service",
    host=HOST.NAME,
    commands=("add_message_to_queue",),
    version=VERSION,
    use_standalone=True,
    standalone_name="msg_q",
)
