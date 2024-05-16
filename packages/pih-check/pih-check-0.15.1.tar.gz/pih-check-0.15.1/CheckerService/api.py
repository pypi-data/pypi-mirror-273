import time
import urllib.request
from typing import Callable
from datetime import datetime
from ssl import SSLCertVerificationError
from urllib.error import URLError, HTTPError

import ipih
from pih.collections import (
    User,
    Result,
    ZabbixMetrics,
    ResourceStatus,
    DiskStatistics,
    WSResourceStatus,
    SiteResourceStatus,
    DisksStatisticsStatus,
    ComputerDescription,
    ServerResourceStatus,
)
from CheckerService.const import *
from pih import A, PIHThreadPoolExecutor
from pih.tools import nn, ne, e, j, js, lw, one


class CheckerApi:

    def __init__(self) -> None:

        self.resources_status_map: dict[str, ResourceStatus] = {}
        self.ws_status_map: dict[str, WSResourceStatus] = {}
        self.server_status_map: dict[str, ServerResourceStatus] = {}
        self.disk_resource_status_map: dict[str, DisksStatisticsStatus] = {}
        self.resources_accessable_map: dict[str, bool] = {}
        self.check_counter: int = 0

        for wappi_profile in A.CT_ME_WH_W.Profiles:
            RESOURCE_LIST.WAPPI.append(
                ResourceStatus(
                    wappi_profile.value,  # type: ignore
                    js(("Профиль Wappi:", wappi_profile.name)),
                    (2, 50, 24 * 60),
                )
            )

        for site_resource_description in A.CT_R_D.SITE_LIST:
            RESOURCE_LIST.SITE.append(
                A.D.fill_data_from_source(
                    SiteResourceStatus(), site_resource_description
                )  # type: ignore
            )

        def filter_function(workstation: ComputerDescription) -> bool:
            return A.C_WS.watchable(workstation)

        def ws_every_action(workstation: ComputerDescription) -> None:
            RESOURCE_LIST.WS.append(
                WSResourceStatus(
                    workstation.name,
                    j(
                        (
                            "Компьютер: ",
                            workstation.name,
                            " (",
                            workstation.description,
                            ")",
                        )
                    ),
                )
            )

        ws_description_result_list: Result[list[ComputerDescription]] = (
            A.R_WS.all_description()
        )
        A.R.every(
            ws_every_action,
            A.R.filter(filter_function, ws_description_result_list, True),
        )

        def server_every_action(server: ComputerDescription) -> None:
            RESOURCE_LIST.SERVER.append(
                ServerResourceStatus(
                    server.name,
                    j(("Сервер: ", server.name, " (", server.description, ")")),
                )
            )

        server_description_result_list: Result[list[ComputerDescription]] = (
            A.R_SRVS.all_description()
        )
        A.R.every(server_every_action, server_description_result_list)

        computer_description_list: list[ComputerDescription] = (
            ws_description_result_list.data + server_description_result_list.data
        )  # type: ignore

        for index in (0, 1):
            RESOURCE_LIST.DISK_STATISTICS_COMPUTER_DESCRIPTION.extend(
                A.D.map(
                    lambda item: (item, index),
                    A.D_FL.computers_with_property(
                        computer_description_list,
                        (
                            A.CT_AD.ComputerProperties.DiskReportable
                            if index == 0
                            else A.CT_AD.ComputerProperties.DiskReportableViaZabbix
                        ),
                    ),
                )
            )

    def send_message_to_it_users(self, message: str) -> None:
        def every_action(user: User) -> None:
            A.ME_WS.to_user(user, message)

        A.R.every(every_action, A.R_U.by_job_position(A.CT_AD.JobPositions.IT))

    def update_resource_status_and_notify(
        self,
        value: ResourceStatus,
        accessable: bool,
        on_init_handler: Callable[[ResourceStatus, bool], None] | None = None,
        on_access_handler: Callable[[ResourceStatus, bool], None] | None = None,
        on_inaccess_handler: Callable[[ResourceStatus, bool], None] | None = None,
    ) -> bool:
        self.resources_accessable_map[value.address] = value.accessable  # type: ignore
        if (
            accessable
            and isinstance(value, SiteResourceStatus)
            and value.check_certificate_status
            and ne(value.certificate_status)
        ):
            accessable = lw(value.certificate_status).find("invalid") == -1
            if accessable:
                pass
        if accessable:
            value.inaccessibility_counter = 0
        else:
            value.inaccessibility_counter += 1
            value.inaccessibility_counter_total += 1
        accessable = A.C_R.accessibility(value)  # type: ignore
        value.accessable = accessable
        if isinstance(value, WSResourceStatus):
            self.ws_status_map[value.address] = value  # type: ignore
        elif isinstance(value, ServerResourceStatus):
            self.server_status_map[value.address] = value  # type: ignore
        else:
            self.resources_status_map[value.address] = value  # type: ignore

        if self.check_counter == value.inaccessibility_check_values[0]:
            if nn(on_init_handler):
                on_init_handler(value, accessable)  # type: ignore
        else:
            if accessable:
                if self.resources_accessable_map[value.address] == False and nn(  # type: ignore
                    on_access_handler
                ):
                    on_access_handler(value, value.inaccessibility_counter == 0)  # type: ignore
            else:
                if (
                    value.inaccessibility_counter
                    <= value.inaccessibility_check_values[0]
                    + value.inaccessibility_check_values[1]
                ) or (
                    value.inaccessibility_counter
                    % value.inaccessibility_check_values[2]
                    == 0
                ):
                    if nn(on_inaccess_handler):
                        on_inaccess_handler(value, self.at_first_time(value))  # type: ignore
        return accessable

    def on_inaccess_handler(
        self, resource_status: ResourceStatus, at_first_time: bool
    ) -> None:
        A.E.resource_inaccessible(resource_status, at_first_time)

    def on_access_handler(
        self, resource_status: ResourceStatus, at_first_time: bool
    ) -> None:
        # if at_first_time:
        A.E.resource_accessible(resource_status, at_first_time)

    def on_init_handler(
        self, resource_status: ResourceStatus, accessable: bool
    ) -> None:
        (
            A.E.resource_accessible(resource_status, True)
            if accessable
            else A.E.resource_inaccessible(resource_status, True)
        )

    def at_first_time(self, resource_status: ResourceStatus) -> bool:
        return (
            resource_status.inaccessibility_counter
            == resource_status.inaccessibility_check_values[0],
        )  # type: ignore

    def set_disk_resource_status(
        self, value: ComputerDescription, via_zabbix: bool = False
    ) -> None:
        def set_disk_statistics_status_for_host(
            host: str, disk_statistics: DiskStatistics
        ) -> None:
            if disk_statistics.size != 0:
                if host not in self.disk_resource_status_map:
                    self.disk_resource_status_map[host] = DisksStatisticsStatus(host)
                self.disk_resource_status_map[host].disk_list.append(disk_statistics)

        disk_statistics_list: list[DiskStatistics] | None = None
        if via_zabbix:
            disk_statistics_map: dict[str, DiskStatistics] = {}
            host_id: int = one(
                A.R.map(
                    lambda item: item.id,
                    A.R.filter(
                        lambda item: lw(item.name) == lw(value.name), A.R_Z.hosts()
                    ),
                )  # type: ignore
            )  # type: ignore

            item_list: list[ZabbixMetrics] = A.R.filter(
                lambda item: item.key_.find("vfs.fs.size") != -1,  # type: ignore
                A.R_Z.items(host_id),
            ).data  # type: ignore
            for item in item_list:
                key_: str = item.key_  # type: ignore
                part_index: int = key_.find(",")
                name: str = key_[key_.find("[") + 1 : part_index - 1]
                type_value: str = key_[part_index + 1 : key_.find("]")]
                if name not in disk_statistics_map:
                    disk_statistics_map[name] = DiskStatistics(name)
                if type_value == "total":
                    disk_statistics_map[name].size = int(item.lastvalue)
                if type_value == "used":
                    disk_statistics_map[name].free_space = disk_statistics_map[
                        name
                    ].size - int(  # type: ignore
                        item.lastvalue
                    )
            disk_statistics_list = A.D.to_list(disk_statistics_map)
        else:
            disk_statistics_list = A.EXC.get_disk_statistics_list(value.name)  # type: ignore
        A.D.every(
            lambda item: set_disk_statistics_status_for_host(value.name, item),  # type: ignore
            disk_statistics_list,
        )

    def ws_or_server_check(
        self,
        resource_status: ResourceStatus,
        check_function: Callable[[ResourceStatus], bool],
        events: tuple[A.CT_E, ...],
    ) -> None:
        def on_access_handler(
            resource_status: ResourceStatus, at_first_time: bool
        ) -> None:
            if at_first_time:
                A.E.send(events[0], (resource_status.address,))

        def on_inaccess_handler(
            resource_status: ResourceStatus, at_first_time: bool
        ) -> None:
            if at_first_time:
                A.E.send(events[1], (resource_status.address,))

        self.update_resource_status_and_notify(
            resource_status,
            check_function(resource_status),
            lambda _, accessable: (
                on_access_handler(resource_status, True)
                if accessable
                else on_inaccess_handler(resource_status, True)
            ),
            on_access_handler,
            on_inaccess_handler,
        )

    def check_resources(
        self, force_update: bool = False, current_datetime: datetime | None = None
    ) -> None:
        start: float = time.perf_counter()
        self.check_counter += 1
        self.action_at_work = True
        #
        self.update_resource_status_and_notify(
            RESOURCE_LIST.INTERNET,
            A.C_R.accessibility_by_ping(RESOURCE_LIST.INTERNET.address, None, 2, False),  # type: ignore
        )
        site_check_free_space_perion_in_minutes: int = (
            A.S_R.site_check_free_space_perion_in_minutes()
        )
        site_check_certificate_start_time: datetime = (
            A.S_R.site_check_certificate_start_time()
        )
        if not RESOURCE_LIST.INTERNET.accessable:
            self.send_message_to_it_users("Вероятно, интернет отсутствует")
        else:

            def check_site(site_resource_status: SiteResourceStatus) -> None:
                site_address: str = site_resource_status.address  # type: ignore
                try:
                    if force_update or ne(current_datetime):
                        if site_resource_status.check_free_space_status:
                            if (
                                e(site_resource_status.free_space_status)
                                or force_update
                                or (
                                    (
                                        (A.SE.life_time.total_seconds() // 60)
                                        % site_check_free_space_perion_in_minutes
                                    )
                                    == 0
                                )
                            ):
                                site_resource_status.free_space_status = A.R_SSH.get_unix_free_space_information_by_drive_name(
                                    site_resource_status.driver_name, site_address  # type: ignore
                                ).data
                        if site_resource_status.check_certificate_status:
                            if (
                                e(site_resource_status.certificate_status)
                                or force_update
                                or (
                                    ne(current_datetime)
                                    and A.D.is_equal_by_time(
                                        current_datetime,  # type: ignore
                                        site_check_certificate_start_time,
                                    )
                                )
                            ):
                                site_resource_status.certificate_status = (
                                    A.R_SSH.get_certificate_information(
                                        site_address
                                    ).data
                                )
                    url: str = j(
                        (
                            A.D.check(
                                site_resource_status.internal,
                                A.CT.UNTRUST_SITE_PROTOCOL,
                                A.CT.SITE_PROTOCOL,
                            ),
                            site_address,
                        )
                    )
                    self.update_resource_status_and_notify(
                        site_resource_status,
                        urllib.request.urlopen(url).getcode() == 200,
                        self.on_init_handler,
                        self.on_access_handler,
                        self.on_inaccess_handler,
                    )
                except URLError as error:
                    if isinstance(error.reason, SSLCertVerificationError):
                        self.update_resource_status_and_notify(
                            site_resource_status, False
                        )
                        A.E.resource_inaccessible(
                            site_resource_status,
                            self.at_first_time(site_resource_status),
                            A.CT_R_IR.CERTIFICATE_ERROR,
                        )

                    if isinstance(error, HTTPError) and error.code == 503:
                        self.update_resource_status_and_notify(
                            site_resource_status, False
                        )
                        A.E.resource_inaccessible(
                            site_resource_status,
                            self.at_first_time(site_resource_status),
                            A.CT_R_IR.SERVICE_UNAVAILABLE,
                        )

            #
            with PIHThreadPoolExecutor(max_workers=len(RESOURCE_LIST.SITE)) as executor:
                for site_resource_status in RESOURCE_LIST.SITE:
                    executor.submit(check_site, site_resource_status)
            #
            for wappi_resource in RESOURCE_LIST.WAPPI:
                self.update_resource_status_and_notify(
                    wappi_resource,
                    A.C_R.wappi_profile_accessibility(wappi_resource.address),  # type: ignore
                    self.on_init_handler,
                    self.on_access_handler,
                    self.on_inaccess_handler,
                )
            #
            if self.update_resource_status_and_notify(
                RESOURCE_LIST.VPN_PACS_SPB,
                A.C_R.vpn_pacs_accessibility(),
                self.on_init_handler,
                self.on_access_handler,
                self.on_inaccess_handler,
            ):
                #
                self.update_resource_status_and_notify(
                    RESOURCE_LIST.PACS_SPB,
                    A.C_R.pacs_accessibility(),
                    self.on_init_handler,
                    self.on_access_handler,
                    self.on_inaccess_handler,
                )
            else:
                self.update_resource_status_and_notify(RESOURCE_LIST.PACS_SPB, False)
        #
        self.update_resource_status_and_notify(
            RESOURCE_LIST.POLIBASE1,
            A.C_R.polibase_accessibility(),
            self.on_init_handler,
            self.on_access_handler,
            self.on_inaccess_handler,
        )
        self.update_resource_status_and_notify(
            RESOURCE_LIST.POLIBASE2,
            A.C_R.polibase_accessibility(test=True),
            self.on_init_handler,
            self.on_access_handler,
            self.on_inaccess_handler,
        )
        if not RESOURCE_LIST.POLIBASE1.accessable:
            self.send_message_to_it_users("Полибейс недоступен")
        #
        with PIHThreadPoolExecutor(max_workers=len(RESOURCE_LIST.WS)) as executor:
            for ws_resource_status in RESOURCE_LIST.WS:
                executor.submit(
                    self.ws_or_server_check,
                    ws_resource_status,
                    lambda resource_status: A.C_R.accessibility_by_smb_port(
                        resource_status.address, count=2, check_all=False
                    ),
                    (
                        A.CT_E.WATCHABLE_WORKSTATION_IS_ACCESSABLE,
                        A.CT_E.WATCHABLE_WORKSTATION_IS_NOT_ACCESSABLE,
                    ),
                )
        #
        with PIHThreadPoolExecutor(max_workers=len(RESOURCE_LIST.SERVER)) as executor:
            for server_resource_status in RESOURCE_LIST.SERVER:
                executor.submit(
                    self.ws_or_server_check,
                    server_resource_status,
                    lambda resource_status: A.C_R.accessibility_by_ping(
                        resource_status.address, count=2, check_all=False
                    ),
                    (A.CT_E.SERVER_IS_ACCESSABLE, A.CT_E.SERVER_IS_NOT_ACCESSABLE),
                )
        #
        self.disk_resource_status_map = {}
        for index in (0, 1):
            computer_list: list[ComputerDescription] = A.D.map(
                lambda item: item[0],
                A.D.filter(
                    lambda item: item[1] == index,
                    RESOURCE_LIST.DISK_STATISTICS_COMPUTER_DESCRIPTION,
                ),
            )  # type: ignore
            with PIHThreadPoolExecutor(max_workers=len(computer_list)) as executor:
                for disk_statistics_computer_description in computer_list:
                    executor.submit(
                        lambda item: self.set_disk_resource_status(item, index == 1),
                        disk_statistics_computer_description,
                    )
        #
        print("Время:", str(time.perf_counter() - start))
        print("Resources", self.resources_status_map)
        print("Disk statistics", self.disk_resource_status_map)
