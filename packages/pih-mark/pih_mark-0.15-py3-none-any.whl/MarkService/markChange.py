import ipih

from pih import A
from pih.collections import Mark, FieldItemList
from pih.tools import FullNameTool

if __name__ == "__main__":
   if A.SE.authenticate():
      A.O.head1("Замена карты")
      actual_mark: Mark = A.I.mark.by_name()
      A.O.value(f"Номер карты, которую будете заменять", actual_mark.TabNumber)
      new_mark: Mark = A.I.mark.free(actual_mark)
      if new_mark:
         A.O.value(f"Номер карты, на которую будете заменять",
                  new_mark.TabNumber)
         A.O.head2("Выберете действие со старой картой доступа")
         _A_: str = A.CT_FNC.AS_FREE
         _B_: str = A.CT_FNC.REMOVE
         _C_: str = A.CT_FNC.CANCEL
         action: str = A.I.indexed_field_list(
             "Введите индекс", FieldItemList(_A_, _B_, _C_))
         if A.I.yes_no("Заменить?"):
               if A.A_M.create(FullNameTool.fullname_from_string(actual_mark.FullName), new_mark.TabNumber, actual_mark.telephoneNumber):
                  A.O.good("Номер карты заменен")
                  if action == _A_:
                     if A.A_M.make_as_free_by_tab_number(actual_mark.TabNumber):
                        A.O.error(f"Карта доступа с табельным номером {actual_mark.TabNumber} преобразована в свободную карту доступа")
                     else:
                        A.O.error("Ошибка при преобразовании в свободную карты доступа")
                  elif action == _B_:
                     if A.A_M.remove(actual_mark):
                        pass
                     else:
                        A.O.error("Ошибка удаления карты доступа")
                  elif action == _C_:
                     pass
                  result = A.R_M.by_name(actual_mark.FullName)
                  A.O.mark.result(
                      result, f"Карты доступа для пользователя {actual_mark.FullName}:")
               else:
                  A.O.error("Ошибка")
         else:
            A.O.error("Отмена") 
