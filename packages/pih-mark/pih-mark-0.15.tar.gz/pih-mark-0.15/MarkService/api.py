import ipih

from pih import A
from pih.consts import (
    MarkType,
    FIELD_COLLECTION,
    FIELD_NAME_COLLECTION,
    FieldCollectionAliases,
)
from MarkService.const import *
from pih.collections import FullName
from pih.tools import escs, j, js, one, ne, nn, n

import contextlib
from datetime import date, datetime
from typing import Any, Tuple
import pymssql


class SQLUpdate:
    def __init__(self, table_name: str, set_string: str, where_statement: Any):
        self.update_statement_string = js(("update", table_name, "set"))
        self.set_string = set_string
        if nn(where_statement):
            if isinstance(where_statement, list) or isinstance(where_statement, Tuple):
                self.where_statement_list = where_statement
            elif isinstance(where_statement, str):
                self.where_statement_list = [where_statement]
        else:
            self.where_statement_list = []

    def to_string(self) -> str:
        if len(self.where_statement_list) > 0:
            where_statement_string = js(
                ("where", j(self.where_statement_list, " and "))
            )
        else:
            where_statement_string = ""
        return js(
            (self.update_statement_string, self.set_string, where_statement_string)
        )


class SQLQuery:
    def __init__(
        self, body: str, where_statement: Any = None, order_by_statement: Any = None
    ):
        SELECT: str = "select"
        self.body = body
        self.select_statement_string = (
            js((SELECT, body)) if body.find(SELECT) != 0 else body
        )

        if nn(where_statement):
            if isinstance(where_statement, list) or isinstance(where_statement, Tuple):
                self.where_statement_list = where_statement
            elif isinstance(where_statement, str):
                self.where_statement_list = [where_statement]
        else:
            self.where_statement_list = []
        if nn(order_by_statement):
            if isinstance(order_by_statement, list):
                self.order_by_statement_list = order_by_statement
            elif isinstance(order_by_statement, str):
                self.order_by_statement_list = [order_by_statement]
        else:
            self.order_by_statement_list = []

    def to_string(self) -> str:
        if len(self.where_statement_list) > 0:
            where_statement_string = js(
                ("where", js(self.where_statement_list, " and"))
            )
        else:
            where_statement_string = ""
        if len(self.order_by_statement_list) > 0:
            order_by_string = js(("order by", js(self.order_by_statement_list, ",")))
        else:
            order_by_string = ""
        return js(
            (self.select_statement_string, where_statement_string, order_by_string)
        )


class OrionApi:
    @staticmethod
    def create_full_name_for_person(tab_number: str, person_type: str) -> FullName:
        return FullName(tab_number, PERSON_FIRST_NAME, person_type)

    @staticmethod
    def create_full_name_for_empty_person(tab_number: str) -> FullName:
        return OrionApi.create_full_name_for_person(
            tab_number, EMPTY_PERSON_MIDDLE_NAME
        )

    @staticmethod
    def create_full_name_for_temporary_person(tab_number: str) -> FullName:
        return OrionApi.create_full_name_for_person(
            tab_number, TEMPORARY_PERSON_MIDDLE_NAME
        )

    @staticmethod
    def get_marks_by_tab_number(value: str) -> list[dict[str, Any]]:
        return OrionApi.query_mark(OrionApi.create_query_for_marks_by_tab_number(value))

    @staticmethod
    def get_marks_by_division_id(value: int) -> list:
        return OrionApi.query_mark(
            OrionApi.create_query_for_marks_by_division_id(value)
        )

    @staticmethod
    def get_mark_by_tab_number(value: str) -> dict[str, Any]:
        return one(OrionApi.get_marks_by_tab_number(value))

    @staticmethod
    def get_marks_by_tab_number_list(value: list[str]) -> list:
        return OrionApi.query_mark(
            OrionApi.create_query_for_marks_by_tab_number_list(value)
        )

    @staticmethod
    def get_marks_by_person_id(value: int) -> dict:
        return OrionApi.query_mark(OrionApi.create_query_for_marks_by_person_id(value))

    @staticmethod
    def create_query_for_marks_by_tab_number(value: str) -> SQLQuery:
        return SQLQuery(
            OrionApi.create_query_for_mark().select_statement_string,
            js((FIELD_NAME_COLLECTION.TAB_NUMBER, "=", escs(value))),
        )

    @staticmethod
    def create_query_for_marks_by_division_id(value: int) -> SQLQuery:
        return SQLQuery(
            OrionApi.create_query_for_mark().select_statement_string,
            js(
                (
                    j(
                        (PERSON_DIVISION_TABLE_NAME_ALIAS, FIELD_NAME_COLLECTION.ID),
                        ".",
                    ),
                    "=",
                    value,
                )
            ),
        )

    @staticmethod
    def create_query_for_marks_by_tab_number_list(value: list[str]) -> SQLQuery:
        condition_value: str = js(A.D.map(escs, value), ",")
        return SQLQuery(
            OrionApi.create_query_for_mark().select_statement_string,
            js((FIELD_NAME_COLLECTION.TAB_NUMBER, "in", "(", condition_value, ")")),
        )

    @staticmethod
    def create_query_for_marks_by_person_id(value: int) -> SQLQuery:
        return SQLQuery(
            OrionApi.create_query_for_mark().select_statement_string,
            js((FIELD_NAME_COLLECTION.ID, "=", value)),
        )

    @staticmethod
    def query_person_by_tab_number(tab_number: str, cursor) -> list:
        result: list = []
        cursor.execute(
            SQLQuery(
                js((FIELD_NAME_COLLECTION.ID, "from", PERSON_LIST_TABLE_NAME)),
                js((FIELD_NAME_COLLECTION.TAB_NUMBER, "=", escs(tab_number))),
            ).to_string()
        )
        for item in cursor:
            result.append(item)
        return result

    @staticmethod
    def decode(value: str) -> str:
        return None if n(value) else value.encode("windows-1252").decode("windows-1251")

    @staticmethod
    def remove_person(id: int) -> None:
        with OrionApi.open_query_connection_and_cursor() as (connection, cursor):
            cursor.execute(
                js(
                    (
                        "delete from",
                        PERSON_LIST_TABLE_NAME,
                        "where",
                        FIELD_NAME_COLLECTION.ID,
                        "= %s",
                    )
                ),
                id,
            )
            connection.commit()

    @staticmethod
    def remove_mark(id: int) -> None:
        with OrionApi.open_query_connection_and_cursor() as (connection, cursor):
            cursor.execute(
                js(
                    (
                        "delete from",
                        MARK_LIST_TABLE_NAME,
                        "where",
                        FIELD_NAME_COLLECTION.ID,
                        "= %s",
                    )
                ),
                id,
            )
            connection.commit()

    @staticmethod
    def remove_person_and_mark(pid: int, mid: int) -> None:
        OrionApi.remove_person(pid)
        OrionApi.remove_mark(mid)

    @staticmethod
    def create_query_connection_and_cursor(charset=DEFAULT_CHARSET) -> None:
        connection = pymssql.connect(
            SERVER,
            USER,
            PASSWORD,
            DB_NAME,
            charset=charset,
            tds_version="7.0"#fuck
        )
        cursor = connection.cursor(as_dict=True)
        return (connection, cursor)

    @staticmethod
    @contextlib.contextmanager
    def open_query_cursor(charset=DEFAULT_CHARSET):
        connection, cursor = OrionApi.create_query_connection_and_cursor(charset)
        try:
            yield cursor
        finally:
            connection.close()

    @staticmethod
    @contextlib.contextmanager
    def open_query_connection_and_cursor(charset=DEFAULT_CHARSET):
        connection, cursor = OrionApi.create_query_connection_and_cursor(charset)
        try:
            yield (connection, cursor)
        finally:
            connection.close()

    @staticmethod
    def person_is_exists_by_tab_number(tab_number: str) -> bool:
        result: bool = False
        with OrionApi.open_query_cursor() as cursor:
            result = len(OrionApi.query_person_by_tab_number(tab_number, cursor)) >= 1
        return result

    @staticmethod
    def get_groups() -> list[dict]:
        return OrionApi.query_for_groups(OrionApi.create_query_for_group_by_name())

    @staticmethod
    def query_for_groups(query_statement: SQLQuery) -> list:
        result: list = []
        with OrionApi.open_query_cursor() as cursor:
            cursor.execute(query_statement.to_string())
            for item in cursor:
                result.append(item)
        return result

    @staticmethod
    def create_query_for_group_by_name(
        group_name: str | None = None, order_by_group_name: bool = True
    ) -> SQLQuery:
        order_by_statement_string: str | None = "Name" if order_by_group_name else None
        where_statement_string: str | None = (
            None if n(group_name) else js(("Name =", escs(group_name)))
        )
        return SQLQuery(
            js(
                (
                    js(
                        (
                            "ID",
                            FIELD_NAME_COLLECTION.NAME,
                            FIELD_NAME_COLLECTION.COMMENT,
                        ),
                        ",",
                    ),
                    "from Groups",
                )
            ),
            where_statement_string,
            order_by_statement_string,
        )

    @staticmethod
    def create_empty_person(tab_number: str) -> None:
        with OrionApi.open_query_connection_and_cursor() as (connection, cursor):
            last_name: str = tab_number
            first_name: str = PERSON_FIRST_NAME
            mid_name: str = EMPTY_PERSON_MIDDLE_NAME
            id: int = 0
            table_name: str = escs(PERSON_LIST_TABLE_NAME)
            cursor.execute(
                js(("select Counter from Counters where TableName =", table_name))
            )
            counter = cursor.fetchone()
            if counter:
                id = int(counter["Counter"]) + 1
            # TODO: find status table
            status = 5
            company = 1
            cursor.execute(
                j(
                    (
                        "insert into ",
                        PERSON_LIST_TABLE_NAME,
                        "(ID, Name, FirstName, MidName, ",
                        FIELD_NAME_COLLECTION.TAB_NUMBER,
                        ", Status, Company) values (",
                        js(
                            (
                                [id]
                                + A.D.map(
                                    escs, (last_name, first_name, mid_name, tab_number)
                                )
                                + [status, company]
                            ),
                            ",",
                        ),
                        ")",
                    )
                )
            )
            cursor.execute(
                js(
                    (
                        "update Counters set Counter =",
                        id,
                        "where TableName =",
                        table_name,
                    )
                )
            )
            connection.commit()

    @staticmethod
    def get_name_search_pattern_for_free_mark_person() -> str:
        return A.D.fullname_to_string(
            FullName(
                ANY_SYMBOL,
                PERSON_FIRST_NAME,
                EMPTY_PERSON_MIDDLE_NAME,
            )
        )

    @staticmethod
    def get_name_search_pattern_for_temporary_mark_person() -> str:
        return A.D.fullname_to_string(
            FullName(
                ANY_SYMBOL,
                PERSON_FIRST_NAME,
                TEMPORARY_PERSON_MIDDLE_NAME,
            )
        )

    @staticmethod
    def get_free_marks():
        return OrionApi.get_marks_by_person_name(
            OrionApi.get_name_search_pattern_for_free_mark_person()
        )

    @staticmethod
    def get_temporary_marks() -> list:
        return OrionApi.query_mark(OrionApi.create_query_for_temporary_marks(), True)

    @staticmethod
    def create_query_for_temporary_marks() -> SQLQuery:
        return SQLQuery(
            f"{PERSON_LIST_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.FULL_NAME}, tt.{FIELD_NAME_COLLECTION.TAB_NUMBER} {FIELD_NAME_COLLECTION.TAB_NUMBER}, {PERSON_LIST_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.TAB_NUMBER} {FIELD_NAME_COLLECTION.OWNER_TAB_NUMBER} from {PERSON_LIST_TABLE_NAME} tt inner join (select {FIELD_NAME_COLLECTION.TAB_NUMBER}, {FIELD_NAME_COLLECTION.ID}, {OrionApi.get_full_name_field(table_alias=None)} from {PERSON_LIST_TABLE_NAME}) {PERSON_LIST_TABLE_NAME_ALIAS} on tt.{FIELD_NAME_COLLECTION.NAME} = {PERSON_LIST_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.TAB_NUMBER}  where {OrionApi.get_full_name_field(None, False)} like '{A.D.fullname_to_string(OrionApi.create_full_name_for_temporary_person(ANY_SYMBOL))}'"
        )

    @staticmethod
    def get_time_tracking(
        begin_datetime: date | None = None,
        end_datetime: date | None = None,
        tab_number_list: list[str] | None = None,
    ) -> list[dict]:
        begin_datetime = begin_datetime or A.D.begin_date()
        end_datetime = end_datetime or A.D.end_date()
        result: list[dict] = []
        datetime_format: str = js((A.CT.ISO_DATE_FORMAT, A.CT.TIME_FORMAT))
        start_date_string: str = A.D.datetime_to_string(begin_datetime, datetime_format)
        end_date_string: str = A.D.datetime_to_string(end_datetime, datetime_format)
        where_statement_list: list[str] = [
            j(
                (
                    LOG_TABLE_NAME,
                    ".HozOrgan=",
                    PERSON_LIST_TABLE_NAME_ALIAS,
                    ".",
                    FIELD_NAME_COLLECTION.ID,
                )
            ),
            j((LOG_TABLE_NAME, "DoorIndex=AcessPoint.GIndex"), "."),
            j((LOG_TABLE_NAME, "Event=Events.Event"), "."),
            j((LOG_TABLE_NAME, "Event=32"), "."),
            js(
                (
                    j(("AcessPoint", FIELD_NAME_COLLECTION.ID), "."),
                    "in",
                    "(",
                    js((34, 35), ","),
                    ")",
                )
            ),
            j(("TimeVal between convert(datetime, ", escs(start_date_string), ", 20)")),
            j(("convert(datetime, ", escs(end_date_string), ", 20)")),
        ]
        if ne(tab_number_list):
            where_statement_list.append(
                js(
                    (
                        FIELD_NAME_COLLECTION.TAB_NUMBER,
                        "in",
                        "(",
                        A.D.list_to_string(tab_number_list, True),
                        ")",
                    )
                )
            )
        query: SQLQuery = SQLQuery(
            f"{OrionApi.get_full_name_field(use_field_alias = True)}, {FIELD_NAME_COLLECTION.TAB_NUMBER}, TimeVal, {PERSON_DIVISION_TABLE_NAME_ALIAS}.Name {FIELD_NAME_COLLECTION.DIVISION_NAME}, {LOG_TABLE_NAME}.Mode Mode from {LOG_TABLE_NAME}, AcessPoint, {PERSON_LIST_TABLE_NAME} {PERSON_LIST_TABLE_NAME_ALIAS} left join {PERSON_DIVISION_TABLE_NAME} {PERSON_DIVISION_TABLE_NAME_ALIAS} on {PERSON_DIVISION_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.ID} = {PERSON_LIST_TABLE_NAME_ALIAS}.{PERSON_DIVISION_FIELD_NAME}, Events",
            where_statement_list,
            "TimeVal desc",
        )
        with OrionApi.open_query_cursor() as cursor:
            cursor.execute(query.to_string())
            for item in cursor:
                result.append(item)
        return result

    @staticmethod
    def get_person_divisions() -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        with OrionApi.open_query_cursor() as cursor:
            cursor.execute(
                SQLQuery(
                    js(
                        (
                            FIELD_NAME_COLLECTION.ID,
                            ",",
                            FIELD_NAME_COLLECTION.NAME,
                            "from",
                            PERSON_DIVISION_TABLE_NAME,
                        )
                    )
                ).to_string()
            )
            for item in cursor:
                result.append(item)
        return result

    @staticmethod
    def get_marks_group_statistics_by_name(
        value: str | None = None, show_guest_marks: bool = False
    ) -> list:
        result: list = []
        with OrionApi.open_query_cursor(UTF8_CHARSET) as cursor:
            query_string: str = js(
                (
                    "select",
                    js(
                        (
                            js(
                                (
                                    FIELD_NAME_COLLECTION.NAME,
                                    FIELD_NAME_COLLECTION.GROUP_NAME,
                                )
                            ),
                            FIELD_NAME_COLLECTION.GROUP_ID,
                            "Count",
                            FIELD_NAME_COLLECTION.COMMENT,
                        ),
                        ",",
                    ),
                    "from (select",
                    js(
                        (
                            FIELD_NAME_COLLECTION.GROUP_ID,
                            j(("Count(", FIELD_NAME_COLLECTION.GROUP_ID, ") as Count")),
                        ),
                        ",",
                    ),
                    "from (",
                )
            )
            query_string += OrionApi.create_query_for_mark_by_person_name(
                value, False
            ).to_string()
            if n(show_guest_marks):
                condition = ""
            elif show_guest_marks:
                condition = f"where {FIELD_NAME_COLLECTION.GROUP_ID} = {GUEST_GROUP_ID}"
            else:
                condition = (
                    f"where {FIELD_NAME_COLLECTION.GROUP_ID} != {GUEST_GROUP_ID}"
                )
            query_string += f") as rt group by {FIELD_NAME_COLLECTION.GROUP_ID}) as rt2 inner join Groups on {FIELD_NAME_COLLECTION.GROUP_ID} = Groups.{FIELD_NAME_COLLECTION.ID} {condition} order by {FIELD_NAME_COLLECTION.GROUP_NAME}"
            cursor.execute(query_string)
            for item in cursor:
                for item_field in item:
                    if item_field in [
                        FIELD_NAME_COLLECTION.GROUP_NAME,
                        FIELD_NAME_COLLECTION.COMMENT,
                    ]:
                        item[item_field] = OrionApi.decode(item[item_field])
                result.append(item)
        return result

    @staticmethod
    def get_free_marks_group_statistics(show_guest_marks: bool = None) -> list:
        return OrionApi.get_marks_group_statistics_by_name(
            OrionApi.get_name_search_pattern_for_free_mark_person(), show_guest_marks
        )

    @staticmethod
    def get_marks_group_statistics() -> list:
        return OrionApi.get_marks_group_statistics_by_name()

    @staticmethod
    def get_free_marks_by_group_id(group_id: int):
        return OrionApi.query_mark(
            OrionApi.create_query_mark_by_name_and_group_id(
                OrionApi.get_name_search_pattern_for_free_mark_person(), group_id
            )
        )

    @staticmethod
    def get_full_name_field(
        table_alias: str = PERSON_LIST_TABLE_NAME_ALIAS, use_field_alias: bool = True
    ) -> str:
        table_alias = "" if n(table_alias) else j((table_alias, "."))
        return f"{table_alias}Name + ' ' + {table_alias}FirstName + ' ' + {table_alias}MidName {FIELD_NAME_COLLECTION.FULL_NAME if use_field_alias else ''}"

    @staticmethod
    def create_query_for_mark() -> SQLQuery:
        return SQLQuery(
            f"{PERSON_LIST_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.ID} {PERSON_LIST_TABLE_NAME_ALIAS}ID, {OrionApi.get_full_name_field()}, m.{FIELD_NAME_COLLECTION.ID} {FIELD_NAME_COLLECTION.MARK_ID}, {FIELD_NAME_COLLECTION.TAB_NUMBER}, g.Name GroupName, g.ID GroupID, g.Comment Comment, WorkPhone {FIELD_NAME_COLLECTION.TELEPHONE_NUMBER}, {PERSON_DIVISION_TABLE_NAME_ALIAS}.Name {FIELD_NAME_COLLECTION.DIVISION_NAME}, {PERSON_DIVISION_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.ID} {FIELD_NAME_COLLECTION.DIVISION_ID} from {PERSON_LIST_TABLE_NAME} {PERSON_LIST_TABLE_NAME_ALIAS} left join {MARK_LIST_TABLE_NAME} m on m.Owner = {PERSON_LIST_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.ID} left join Groups g on g.{FIELD_NAME_COLLECTION.ID} = Group{FIELD_NAME_COLLECTION.ID} left join {PERSON_DIVISION_TABLE_NAME} {PERSON_DIVISION_TABLE_NAME_ALIAS} on {PERSON_LIST_TABLE_NAME_ALIAS}.{PERSON_DIVISION_FIELD_NAME} = {PERSON_DIVISION_TABLE_NAME_ALIAS}.{FIELD_NAME_COLLECTION.ID}"
        )

    @staticmethod
    def create_update_for_person_by_tab_number(
        value: str, set_string: str
    ) -> SQLUpdate:
        return SQLUpdate(
            PERSON_LIST_TABLE_NAME,
            set_string,
            j((FIELD_NAME_COLLECTION.TAB_NUMBER, "=", escs(value))),
        )

    @staticmethod
    def update_for_person_by_tab_number(value: str, set_string: str) -> None:
        with OrionApi.open_query_connection_and_cursor(UTF8_CHARSET) as (
            connection,
            cursor,
        ):
            cursor.execute(
                OrionApi.create_update_for_person_by_tab_number(
                    value, set_string
                ).to_string()
            )
            connection.commit()

    @staticmethod
    def update_person_full_name_by_tab_number_set_string(full_name: FullName) -> str:
        return js(
            (
                j(("Name=", escs(full_name.last_name))),
                j(("FirstName=", escs(full_name.first_name))),
                j(("MidName=", escs(full_name.middle_name))),
            ),
            ",",
        )

    @staticmethod
    def update_person_full_name_and_division_by_tab_number(
        full_name: FullName, person_division_id: int, tab_number: str
    ) -> None:
        OrionApi.update_for_person_by_tab_number(
            tab_number,
            js(
                (
                    OrionApi.update_person_full_name_by_tab_number_set_string(
                        full_name
                    ),
                    js((PERSON_DIVISION_FIELD_NAME, "=", person_division_id)),
                ),
                ",",
            ),
        )

    @staticmethod
    def update_person_full_name_by_tab_number(
        full_name: FullName, tab_number: str
    ) -> None:
        OrionApi.update_for_person_by_tab_number(
            tab_number,
            OrionApi.update_person_full_name_by_tab_number_set_string(full_name),
        )

    @staticmethod
    def update_telephone_number_by_tab_number(value: str, tab_number: str) -> None:
        OrionApi.update_for_person_by_tab_number(
            tab_number, j(("WorkPhone=", escs(value)))
        )

    @staticmethod
    def create_query_for_mark_by_person_name(
        name: str | None = None, order_by_name: bool = True
    ) -> SQLQuery:
        order_by_statement_string: str = (
            js((FIELD_NAME_COLLECTION.FULL_NAME, FIELD_NAME_COLLECTION.TAB_NUMBER), ",")
            if order_by_name
            else None
        )
        where_statement_string: str = (
            js(
                (
                    OrionApi.get_full_name_field(use_field_alias=False),
                    "like",
                    escs(name),
                )
            )
            if name
            else None
        )
        return SQLQuery(
            OrionApi.create_query_for_mark().select_statement_string,
            where_statement_string,
            order_by_statement_string,
        )

    @staticmethod
    def create_query_mark_by_name_and_group_id(
        name: str | None = None, group_id: int = None
    ) -> SQLQuery:
        query: SQLQuery = OrionApi.create_query_for_mark_by_person_name(name, False)
        query.where_statement_list.append(
            j(("g.", FIELD_NAME_COLLECTION.ID, "=", group_id))
        )
        query.order_by_statement_list = [FIELD_NAME_COLLECTION.TAB_NUMBER]
        return query

    @staticmethod
    def get_marks_by_person_name(value: str) -> list:
        if value == "":
            value = ANY_SYMBOL
        else:
            value = j((ANY_SYMBOL, value, ANY_SYMBOL))
        return OrionApi.query_mark(OrionApi.create_query_for_mark_by_person_name(value))

    @staticmethod
    def query_mark(query: SQLQuery, fetch_only_full_name: bool = False) -> list:
        result: list = []
        fields: list = [FIELD_NAME_COLLECTION.FULL_NAME]
        if not fetch_only_full_name:
            fields += [
                FIELD_NAME_COLLECTION.GROUP_NAME,
                FIELD_NAME_COLLECTION.COMMENT,
                FIELD_NAME_COLLECTION.DIVISION_NAME,
            ]
        with OrionApi.open_query_cursor(UTF8_CHARSET) as cursor:
            try:
                query_string = query.to_string()
                cursor.execute(query_string)
                for item in cursor:
                    for item_field in item:
                        if item_field in fields:
                            item[item_field] = OrionApi.decode(item[item_field])
                    if not fetch_only_full_name:
                        full_name: str = item[FIELD_NAME_COLLECTION.FULL_NAME]
                        tab_number: str = item[FIELD_NAME_COLLECTION.TAB_NUMBER]
                        type: MarkType = MarkType.NORMAL
                        if OrionApi.guest(item[FIELD_NAME_COLLECTION.GROUP_ID]):
                            type = MarkType.GUEST
                        elif OrionApi.free(tab_number, full_name):
                            type = MarkType.FREE
                        elif OrionApi.temporary(tab_number, full_name):
                            type = MarkType.TEMPORARY
                        item[FIELD_NAME_COLLECTION.TYPE] = type
                    result.append(item)
            except Exception as error:
                print(error)
        return result

    @staticmethod
    def free(tab_number: str, name: str) -> bool:
        return A.D.is_equal_by_fullname(
            A.D.fullname_from_string(name),
            OrionApi.create_full_name_for_empty_person(tab_number),
        )

    @staticmethod
    def guest(group_id: int) -> bool:
        return group_id == GUEST_GROUP_ID

    @staticmethod
    def temporary(tab_number: str, name: str) -> bool:
        return A.D.to_given_name(A.D.fullname_from_string(name)) == A.D.to_given_name(
            OrionApi.create_full_name_for_temporary_person(tab_number)
        )

    @staticmethod
    def get_tab_number_for_temporary_mark(mark: dict) -> str:
        return A.D_Ex.as_full_name(mark).last_name

    class INPUT:
        @staticmethod
        def tab_number(check: bool = True) -> str:
            return A.I.tab_number(check)

        @staticmethod
        def name() -> str:
            return A.I.name()

    class ACTION:
        @staticmethod
        def remove_person_and_mark(data: dict) -> bool:
            pid: int = int(A.D_Ex.person_id(data))
            mid: int = int(A.D_Ex.mark_id(data))
            try:
                OrionApi.remove_person_and_mark(pid, mid)
                return True
            except:
                return False

        @staticmethod
        def make_mark_as_temporary(
            temporary_tab_number: str, owner_tab_number: str
        ) -> bool:
            temporary_mark: dict[str, Any] | None = OrionApi.get_mark_by_tab_number(
                temporary_tab_number
            )
            owner_mark: dict[str, Any] | None = OrionApi.get_mark_by_tab_number(
                owner_tab_number
            )
            if temporary_mark and owner_mark:
                OrionApi.update_person_full_name_by_tab_number(
                    OrionApi.create_full_name_for_temporary_person(owner_tab_number),
                    temporary_tab_number,
                )
                return True
            else:
                return False

        @staticmethod
        def remove_mark_by_tab_number(value: str) -> bool:
            mark: dict[str, Any] | None = OrionApi.get_mark_by_tab_number(value)
            if n(mark):
                return None
            else:
                return OrionApi.ACTION.remove_person_and_mark(mark)

        @staticmethod
        def create_empty_person(tab_number: str) -> bool:
            try:
                OrionApi.create_empty_person(tab_number)
                return True
            except:
                return False

        @staticmethod
        def update_person_full_name_and_division_by_tab_number(
            full_name: FullName, person_division_id: int, tab_number: str
        ) -> bool:
            try:
                OrionApi.update_person_full_name_and_division_by_tab_number(
                    full_name, person_division_id, tab_number
                )
                return True
            except:
                return False

        @staticmethod
        def update_telephone_number_by_tab_number(value: str, tab_number: str) -> bool:
            try:
                OrionApi.update_telephone_number_by_tab_number(value, tab_number)
                return True
            except:
                return False

        @staticmethod
        def make_mark_as_free_by_tab_number(tab_number: str) -> bool:
            if OrionApi.CHECK.person_exists_by_tab_number(tab_number):
                return (
                    OrionApi.ACTION.update_person_full_name_and_division_by_tab_number(
                        OrionApi.create_full_name_for_empty_person(tab_number),
                        0,
                        tab_number,
                    )
                    and OrionApi.ACTION.update_telephone_number_by_tab_number(
                        "", tab_number
                    )
                )
            else:
                return None

        @staticmethod
        def create_mark(
            full_name: FullName,
            person_division_id: int,
            tab_number: str,
            telephone: str | None = None,
        ) -> bool:
            result: bool = False
            if OrionApi.ACTION.update_person_full_name_and_division_by_tab_number(
                full_name, person_division_id, tab_number
            ):
                if OrionApi.ACTION.update_telephone_number_by_tab_number(
                    telephone if telephone else "", tab_number
                ):
                    result = True
            return result

    class CHECK:
        @staticmethod
        def person_exists_by_tab_number(value: str) -> bool:
            return OrionApi.person_is_exists_by_tab_number(value)

        @staticmethod
        def mark_exists_by_tab_number(value: str) -> bool:
            return ne(OrionApi.get_mark_by_tab_number(value))

        @staticmethod
        def free(tab_number: str) -> bool:
            mark = OrionApi.get_mark_by_tab_number(tab_number)
            return A.D.check_not_none(
                mark,
                lambda: OrionApi.free(
                    mark[FIELD_NAME_COLLECTION.TAB_NUMBER],
                    mark[FIELD_NAME_COLLECTION.FULL_NAME],
                ),
            )

        @staticmethod
        def guest(tab_number: str) -> bool:
            mark = OrionApi.get_mark_by_tab_number(tab_number)
            return A.D.check_not_none(
                mark, lambda: OrionApi.guest(mark[FIELD_NAME_COLLECTION.GROUP_ID])
            )

        @staticmethod
        def temporary(tab_number: str) -> bool:
            mark = OrionApi.get_mark_by_tab_number(tab_number)
            return A.D.check_not_none(
                mark, lambda: OrionApi.temporary(mark[FIELD_NAME_COLLECTION.GROUP_ID])
            )

        @staticmethod
        def can_be_created(tab_number: str) -> bool:
            mark: dict[str, Any] = OrionApi.get_mark_by_tab_number(tab_number)
            return not (
                OrionApi.CHECK.free(mark)
                or OrionApi.CHECK.guest(mark)
                or OrionApi.CHECK.temporary(mark)
            )

        @staticmethod
        def need_strip(value: str) -> bool:
            return value.strip() != value

        @staticmethod
        def name(value: str) -> bool:
            return not OrionApi.CHECK.need_strip(value)

    class RESULT:
        @staticmethod
        def time_tracking(
            start_date: datetime, end_date: datetime, tab_number_list: list[str] = None
        ) -> dict:
            data: list[dict] = OrionApi.get_time_tracking(
                start_date, end_date, tab_number_list
            )
            mark_list: list[dict] = list(
                filter(
                    lambda item: OrionApi.temporary(
                        item[FIELD_NAME_COLLECTION.TAB_NUMBER],
                        item[FIELD_NAME_COLLECTION.FULL_NAME],
                    ),
                    data,
                )
            )
            mark_cache: dict | None = None
            if ne(mark_list):
                mark_cache = {
                    mark[FIELD_NAME_COLLECTION.TAB_NUMBER]: mark
                    for mark in OrionApi.get_marks_by_tab_number_list(
                        list(
                            set(
                                A.D.map(
                                    OrionApi.get_tab_number_for_temporary_mark,
                                    mark_list,
                                )
                            )
                        )
                    )
                }
            for item in data:
                full_name: str = item[FIELD_NAME_COLLECTION.FULL_NAME]
                tab_number: str = item[FIELD_NAME_COLLECTION.TAB_NUMBER]
                if mark_cache and tab_number in mark_cache:
                    owner_mark = mark_cache[tab_number]
                    item[FIELD_NAME_COLLECTION.TAB_NUMBER] = tab_number
                    item[FIELD_NAME_COLLECTION.FULL_NAME] = full_name
                    item[FIELD_NAME_COLLECTION.DIVISION_NAME] = owner_mark[
                        FIELD_NAME_COLLECTION.DIVISION_NAME
                    ]
            return A.R.pack(FieldCollectionAliases.TIME_TRACKING, data)

        @staticmethod
        def owner_mark_for_temporary_mark(tab_number: str) -> list:
            mark = OrionApi.get_mark_by_tab_number(tab_number)
            return OrionApi.RESULT.by_tab_number(
                OrionApi.get_tab_number_for_temporary_mark(mark)
            )

        @staticmethod
        def person_divisions() -> dict:
            return A.R.pack(
                FieldCollectionAliases.PERSON_DIVISION, OrionApi.get_person_divisions()
            )

        @staticmethod
        def by_division_id(value: int) -> dict:
            return A.R.pack(
                FieldCollectionAliases.PERSON_DIVISION,
                OrionApi.get_marks_by_division_id(value),
            )

        @staticmethod
        def all_marks() -> dict:
            return OrionApi.RESULT.by_name("")

        @staticmethod
        def by_name(name: str) -> dict:
            return A.R.pack(
                FieldCollectionAliases.PERSON_EXTENDED,
                OrionApi.get_marks_by_person_name(name),
            )

        @staticmethod
        def free_marks() -> dict:
            return A.R.pack(FIELD_COLLECTION.ORION.FREE_MARK, OrionApi.get_free_marks())

        @staticmethod
        def free_marks_by_group_id(value: int) -> dict:
            return A.R.pack(
                FIELD_COLLECTION.ORION.TAB_NUMBER_BASE,
                OrionApi.get_free_marks_by_group_id(value),
            )

        @staticmethod
        def free_marks_group_statistics(show_guest_marks: bool = None) -> dict:
            return A.R.pack(
                FIELD_COLLECTION.ORION.GROUP_STATISTICS,
                OrionApi.get_free_marks_group_statistics(show_guest_marks),
            )

        @staticmethod
        def marks_group_statistics() -> dict:
            return A.R.pack(
                FIELD_COLLECTION.ORION.GROUP_STATISTICS,
                OrionApi.get_marks_group_statistics(),
            )

        @staticmethod
        def by_tab_number(value: str | None = None) -> dict:
            return A.R.pack(
                FieldCollectionAliases.PERSON,
                A.D.check_not_none(
                    value, lambda: OrionApi.get_mark_by_tab_number(value), None
                ),
            )

        @staticmethod
        def by_person_id(value: int) -> dict:
            return A.R.pack(
                FieldCollectionAliases.PERSON, OrionApi.get_marks_by_person_id(value)
            )

        @staticmethod
        def temporary_marks() -> dict[str, Any]:
            return A.R.pack(
                FieldCollectionAliases.TEMPORARY_MARK, OrionApi.get_temporary_marks()
            )

        @staticmethod
        def groups() -> list:
            return A.R.pack(FIELD_COLLECTION.ORION.GROUP, OrionApi.get_groups())
