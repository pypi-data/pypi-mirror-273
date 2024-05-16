import ipih

from pih import A
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription
from pih.collections import ResourceStatus, ComputerDescription, SiteResourceStatus

NAME: str = "Checker"

HOST = Hosts.BACKUP_WORKER.NAME

VERSION: str = "0.15.1"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Checker service",
    host=HOST,
    commands=("get_resource_status_list",),
    standalone_name="check",
    use_standalone=True,
    version=VERSION,
)


class RESOURCE_LIST:

    INTERNET: ResourceStatus = A.D.fill_data_from_source(
        ResourceStatus(), A.CT_R_D.INTERNET
    )

    VPN_PACS_SPB: ResourceStatus = A.D.fill_data_from_source(
        ResourceStatus(), A.CT_R_D.VPN_PACS_SPB
    )

    #PACS_SPB: ResourceStatus = A.D.fill_data_from_source(
    #    ResourceStatus(), A.CT_R_D.PACS_SPB
    #)

    SITE: list[SiteResourceStatus] = []

    WAPPI: list[ResourceStatus] = []

    WS: list[ResourceStatus] = []

    SERVER: list[ResourceStatus] = []

    POLIBASE1: ResourceStatus = A.D.fill_data_from_source(
        ResourceStatus(), A.CT_R_D.POLIBASE1
    )

    POLIBASE2: ResourceStatus = A.D.fill_data_from_source(
        ResourceStatus(), A.CT_R_D.POLIBASE2
    )

    DISK_STATISTICS_COMPUTER_DESCRIPTION: list[tuple[ComputerDescription, int]] = []
