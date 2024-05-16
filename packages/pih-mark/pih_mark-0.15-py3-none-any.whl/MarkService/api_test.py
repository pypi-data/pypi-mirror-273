

from datetime import datetime
from api import Orion as Api
from pih.collections import FullName

import time
from pih.const import FIELD_NAME_COLLECTION

from pih import A, j, js

"""
print(Orion.CHECK.person_is_exists_by_tab_number("175"))
print(Orion.CHECK.mark_is_exists_by_tab_number("175"))

print(Orion.CHECK.is_free("119"))
print(",",Orion.CHECK.is_guest("175"))
print(Orion.CHECK.is_temporary("1583"))

print(Orion.RESULT.temporary_marks())
print(Orion.RESULT.by_tab_number("015"))
"""

from pih.collections import TimeTrackingEntity
import schedule

print(A.D.fill_data_from_list_source(TimeTrackingEntity, Api.get_time_tracking()))

cache: dict = {}

def tt_report() -> None:
    now: datetime = A.D.now()
    time_tracking_item: TimeTrackingEntity | None = None
    for time_tracking_item in A.D.fill_data_from_list_source(TimeTrackingEntity, Api.get_time_tracking(now.replace(second=0), now.replace(second=59))):
        time_tracking_item_name: str = j((time_tracking_item.FullName, time_tracking_item.Mode, time_tracking_item.TimeVal.date()), ":")
        if time_tracking_item_name not in cache:
            A.L.time_tracking(js((js(("Сотрудник", time_tracking_item.FullName)), "отметился на приход" if time_tracking_item.Mode == 1 else "отметился на выход")))
            cache[time_tracking_item_name] = time_tracking_item
        else:
            cached_tt_item: TimeTrackingEntity = cache[time_tracking_item_name] 


schedule.every(5).seconds.do(tt_report)
while True:
    schedule.run_pending()
    time.sleep(1)

