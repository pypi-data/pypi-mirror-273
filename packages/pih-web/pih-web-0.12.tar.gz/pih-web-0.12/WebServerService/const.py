import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "WebServer"

HOST = Hosts.WS255

PACKAGES: tuple[str, ...] = ("fastapi", "uvicorn", "python-multipart", "dicttoxml")

VERSION: str = "0.12"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Web Server service",
    host=HOST.NAME,
    use_standalone=True,
    standalone_name="web",
    version=VERSION,
    host_changeable=False,
    packages=PACKAGES,
)