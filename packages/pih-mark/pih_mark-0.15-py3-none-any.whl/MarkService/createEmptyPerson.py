import ipih
from pih import A
from api import OrionApi as Api

if __name__ == "__main__":
    try:
        tab_number: str = A.I.tab_number()
        if A.C_M.tab_number(tab_number):
            if Api.CHECK.person_exists_by_tab_number(tab_number):
                A.O.error("Карта доступа с табельным номером уже в есть!")
            else:
                if A.I.yes_no("Создать?", True):
                    if Api.ACTION.create_empty_person(tab_number):
                        A.O.good("Пустая персона создана")
                    else:
                        A.O.error("Ошибка при создании пустой персона")
                else:
                    A.O.error("Отмена!")
    except KeyboardInterrupt:
        pass