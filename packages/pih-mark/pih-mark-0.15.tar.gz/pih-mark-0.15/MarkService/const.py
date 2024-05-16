import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "Mark"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.15"

PACKAGES: tuple[str, ...] = ("pymssql", "schedule")

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Orion service",
    host=HOST.NAME,
    commands=(
        "get_free_mark_list",
        "get_temporary_mark_list",
        "get_mark_person_division_list",
        "get_time_tracking",
        "get_mark_list",
        "get_mark_by_tab_number",
        "get_mark_by_person_name",
        "get_free_mark_group_statistics_list",
        "get_free_mark_list_by_group_id",
        "get_owner_mark_for_temporary_mark",
        "get_mark_list_by_division_id",
        "set_full_name_by_tab_number",
        "set_telephone_by_tab_number",
        "check_mark_free",
        "create_mark",
        "make_mark_as_free_by_tab_number",
        "make_mark_as_temporary",
        "remove_mark_by_tab_number",
    ),
    version=VERSION,
    standalone_name="mark",
    use_standalone=True,
    packages=PACKAGES,
)


SERVER: str = r"orion\SQLEXPRESS"
USER: str = "sa"
PASSWORD: str = "123456"
DB_NAME: str = "Orion1"
DEFAULT_CHARSET: str = "cp1251"
UTF8_CHARSET: str = "utf8"
PERSON_LIST_TABLE_NAME: str = "pList"
PERSON_LIST_TABLE_NAME_ALIAS: str = PERSON_LIST_TABLE_NAME[0]
LOG_TABLE_NAME: str = "pLogData"
PERSON_DIVISION_TABLE_NAME: str = "PDivision"
PERSON_DIVISION_TABLE_NAME_ALIAS: str = "pd"
PERSON_DIVISION_FIELD_NAME: str = "Section"
MARK_LIST_TABLE_NAME: str = "pMark"
PERSON_FIRST_NAME: str = "__person__"
EMPTY_PERSON_MIDDLE_NAME: str = "__empty__"
TEMPORARY_PERSON_MIDDLE_NAME: str = "__temporary__"
ANY_SYMBOL: str = "%"
GUEST_GROUP_ID: int = 60
