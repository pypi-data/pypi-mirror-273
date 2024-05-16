import ipih

from pih import A, PIHThread
from MarkService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih.tools import ParameterList, j
        from MarkService.api import OrionApi as Api
        from pih.collections import FullName, TimeTrackingEntity

        from datetime import datetime
        from typing import Any
        import schedule
        import time

        class DH:
            time_tracking_cache: dict[str, TimeTrackingEntity] = {}

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.get_free_mark_list:
                return Api.RESULT.free_marks()
            if sc == SC.get_free_mark_group_statistics_list:
                return Api.RESULT.free_marks_group_statistics(pl.next())
            if sc == SC.get_free_mark_list_by_group_id:
                return Api.RESULT.free_marks_by_group_id(pl.next())
            if sc == SC.get_mark_by_tab_number:
                return Api.RESULT.by_tab_number(pl.next())
            if sc == SC.get_mark_by_person_name:
                return Api.RESULT.by_name(pl.next())
            if sc == SC.get_mark_list_by_division_id:
                return Api.RESULT.by_division_id(pl.next())
            if sc == SC.set_full_name_by_tab_number:
                return Api.ACTION.update_person_full_name_and_division_by_tab_number(
                    pl.next(FullName()), pl.next()
                )
            if sc == SC.set_telephone_by_tab_number:
                return Api.ACTION.update_telephone_number_by_tab_number(
                    pl.next(), pl.next()
                )
            if sc == SC.make_mark_as_free_by_tab_number:
                return Api.ACTION.make_mark_as_free_by_tab_number(pl.next())
            if sc == SC.remove_mark_by_tab_number:
                return Api.ACTION.remove_mark_by_tab_number(pl.next())
            if sc == SC.get_mark_person_division_list:
                return Api.RESULT.person_divisions()
            if sc == SC.get_mark_list:
                return Api.RESULT.all_marks()
            if sc == SC.check_mark_free:
                return Api.CHECK.free(pl.next())
            if sc == SC.create_mark:
                return Api.ACTION.create_mark(
                    pl.next(FullName()),
                    pl.next(),
                    pl.next(),
                    pl.next(),
                )
            if sc == SC.get_time_tracking:
                return Api.RESULT.time_tracking(
                    A.D.datetime_from_string(pl.next()),
                    A.D.datetime_from_string(pl.next()),
                    pl.next(),
                )
            if sc == SC.make_mark_as_temporary:
                return Api.ACTION.make_mark_as_temporary(pl.next(), pl.next())
            if sc == SC.get_temporary_mark_list:
                return Api.RESULT.temporary_marks()
            if sc == SC.get_owner_mark_for_temporary_mark:
                return Api.RESULT.owner_mark_for_temporary_mark(pl.next())
            if sc == SC.door_command:
                return door_operation(pl.next(), pl.next())

        def service_starts_handler() -> None:
            PIHThread(time_tracking_log_handler)

        def time_tracking_log_handler() -> None:
            def time_tracking_logger() -> None:
                now: datetime = A.D.now()
                time_tracking_item: TimeTrackingEntity | None = None
                print(
                    now.replace(minute=max(0, now.minute - 1)),
                    now.replace(minute=min(59, now.minute + 1)),
                )
                for time_tracking_item in A.D.fill_data_from_list_source(
                    TimeTrackingEntity,
                    Api.get_time_tracking(
                        now.replace(minute=max(0, now.minute - 1)),
                        now.replace(minute=min(59, now.minute + 1)),
                    ),
                ):
                    time_tracking_item_name: str = j(
                        (
                            time_tracking_item.FullName,
                            time_tracking_item.Mode,
                            time_tracking_item.TimeVal.date(),
                        ),
                        ":",
                    )
                    checked_in: bool = time_tracking_item.Mode == 1
                    if time_tracking_item_name not in DH.time_tracking_cache:
                        DH.time_tracking_cache[time_tracking_item_name] = (
                            time_tracking_item
                        )
                        A.E.send(
                            (
                                A.CT_E.EMPLOYEE_CHECKED_IN
                                if checked_in
                                else A.CT_E.EMPLOYEE_CHECKED_OUT
                            ),
                            (time_tracking_item.FullName,),
                        )

            schedule.every(5).seconds.do(time_tracking_logger)
            while True:
                schedule.run_pending()
                time.sleep(1)

        @staticmethod
        def door_operation(door_name: str, operation_name: str) -> bool:
            return A.D_Ex.returncode(A.EXC.execute(
                A.EXC.create_command_for_psexec(
                    (
                        A.CT_WINDOWS.SERVICES.TASK_SCHEDULER,
                        "/run",
                        "/tn",
                        j((door_name, "_door_", operation_name)),
                    ),
                    A.CT_H.ORION.NAME,
                    run_from_system_account=True,
                    interactive=None,
                    use_raw_host_name=True,
                    use_raw_login=True,
                ),
                True,
            ))

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
