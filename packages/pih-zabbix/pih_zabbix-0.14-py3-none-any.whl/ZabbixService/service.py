import ipih

from pih import A
from pih.tools import j
from ZabbixService.const import *
from pih.consts.zabbix import ZABBIX

from zabbix_utils import Sender


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        from typing import Any
        from pih.tools import ParameterList

        from pyzabbix.api import ZabbixAPI

        class DH:
            zabbix: ZabbixAPI | None = None

        SC = A.CT_SC

        ISOLATED: bool = False

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.serve_command:
                command: ZABBIX.Commands = pl.next(ZABBIX.Commands)
                if command == ZABBIX.Commands.get_host_list:
                    return A.R.pack(
                        None,
                        [
                            {
                                A.CT_FNC.ID: item["hostid"],
                                A.CT_FNC.NAME: item[A.CT_FNC.NAME],
                                A.CT_FNC.HOST: item[A.CT_FNC.HOST],
                            }
                            for item in DH.zabbix.host.get(output="extend")
                        ],
                    )
                if command == ZABBIX.Commands.send_value:
                    return (
                        Sender(server=ZABBIX_SERVER_HOST, port=ZABBIX_SERVER_PORT)
                        .send_value(pl.next(), pl.next(), pl.next(), A.D.timestamp())
                        .failed
                        == 0
                    )
                if command == ZABBIX.Commands.get_item_list:
                    return A.R.pack(
                        None,
                        DH.zabbix.item.get(
                            hostids=pl.next(),
                            itemids=pl.next(),
                            output=pl.next() or "extend",
                        ),
                    )
                if command == ZABBIX.Commands.get_value_list:
                    return A.R.pack(
                        None,
                        DH.zabbix.history.get(
                            hostids=[pl.next()],
                            itemids=[pl.next()],
                            sortfield="clock",
                            sortorder="DESC",
                            limit=pl.next(),
                            output="extend",
                        ),
                    )

        def service_starts_handler() -> None:
            zabbix_server_url: str = j(
                (
                    A.CT.UNTRUST_SITE_PROTOCOL,
                    ZABBIX_SERVER_HOST,
                    A.CT.SPLITTER,
                    ZABBIX_SERVER_WEB_INTERFACE_PORT,
                )
            )
            zabbix = ZabbixAPI(zabbix_server_url)
            zabbix.login(ZABBIX_SERVER_LOGIN, ZABBIX_SERVER_PASSWORD)
            DH.zabbix = zabbix

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
