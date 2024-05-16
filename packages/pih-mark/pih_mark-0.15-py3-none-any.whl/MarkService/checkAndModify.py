from typing import List
import colorama
from colorama import Back
from api import OrionApi

import ipih

from pih import A


MODIFY = False

if __name__ == "__main__":

    colorama.init()

    with OrionApi.open_query_connection_and_cursor() as (connection, cursor):
        cursor.execute("select l.*, m.ID pMark_ID, m.Gtype, m.GTypeCodeAdd, m.Config, m.Status, m.grStatus, m.GroupID, l.TabNumber TabNumber from pList l right outer join pMark m on l.ID = m.Owner order by l.Name, l.FirstName, l.MidName;")
        mark_list:List = []
        print(f"{Back.CYAN}Персона с карточкой:{Back.RESET}")
        for value in cursor:
            mark_list.append(value)
        for value in mark_list:
            tab_number = str(value["TabNumber"])
            lastname = value["Name"]
            firstname = value["FirstName"]
            middlename = value["MidName"]
            need_to_be_modificated_list: List = []
            need_to_be_modificated: str = ""
            if not OrionApi.CHECK.name(lastname):
                need_to_be_modificated_list.append("lastname")
            if not OrionApi.CHECK.name(firstname):
                need_to_be_modificated_list.append("firstname")
            if not OrionApi.CHECK.name(middlename):
                need_to_be_modificated_list.append("middlename")
            if not A.C_M.tab_number(tab_number):
                need_to_be_modificated_list.append("Invalid tab number")
            if(len(need_to_be_modificated_list) > 0):
                need_to_be_modificated = f"{Back.RED}needModificate: {', '.join(need_to_be_modificated_list)}{Back.RESET}"
            print(
                f"{tab_number}: {lastname} {firstname} {middlename} {need_to_be_modificated}")
        #
        print(f"{Back.CYAN}Записи c уровнем доступа 'Запрет':{Back.RESET}")
        cursor.execute("select m.ID mID, l.ID lID, Name, FirstName, MidName from pMark m inner join pList l on m.Owner = l.ID where GroupID = 1 order by Name, FirstName, MidName;")
        index = 0
        for value in cursor:
            index += 1
            id = str(value["lID"])
            lastname = value["Name"]
            firstname = value["FirstName"]
            middlename = value["MidName"]
            print(f"{Back.RED}{id} : {lastname} {firstname} {middlename}{Back.RESET}")
        if index == 0:
            print(f"{Back.GREEN}Нет записей с запретом{Back.RESET}")
        #
        print(f"{Back.CYAN}Записи без уровня доступа{Back.RESET}")
        cursor.execute("select l.*, m.ID as pMark_ID, m.Gtype, m.GTypeCodeAdd, m.Config, m.Status, m.grStatus, m.GroupID from pList l right outer join pMark m on l.ID = m.Owner where m.GroupID = -1 order by l.Name, l.FirstName, l.MidName;")
        index = 0
        for value in cursor:
            index += 1
            id = str(value["ID"])
            lastname = value["Name"]
            firstname = value["FirstName"]
            middlename = value["MidName"]
            print(
                f"    {Back.RED}{id} : {lastname} {firstname} {middlename}{Back.RESET}")
        if index == 0:
            print(f"{Back.GREEN}Нет записей без уровня доступа{Back.RESET}")
        #
        print(f"{Back.CYAN}Персона без карточки:{Back.RESET}")
        cursor.execute(
            "select * from pList l where not exists (select 1 from pMark m where l.ID = m.Owner) order by l.Name, l.FirstName, l.MidName;")
        markless_list:List = []
        for value in cursor:
            markless_list.append(value)
        if len(markless_list) != 0:
            markless_removed_file = open("marklessRemoved.txt", "a")
            for value in markless_list:
                id = str(value["ID"])
                lastname = value["Name"]
                firstname = value["FirstName"]
                middlename = value["MidName"]
                print(f"{id}: {lastname} {firstname} {middlename}")
                if MODIFY:
                    cursor.execute(f"delete from pList where ID='{id}';")
                markless_removed_file.write(f"{str(value)}\n")
            markless_removed_file.close()
        else:
            print(f"{Back.GREEN}Не найдено{Back.RESET}")
        connection.commit()
        #
        print(f"{Back.CYAN}Все уровни доступа:{Back.RESET}")
        cursor.execute("select * from Groups order by name")
        group_list = []
        for value in cursor:
            group_list.append(value)
        if len(group_list) != 0:
            for value in group_list:
                id = str(value["ID"])
                print(f"    {id}: {value['Name']}")
        else:
            print(f"{Back.RED}Не найдено{Back.RESET}")
        #
        print(f"{Back.CYAN}Все уровни доступа для имеющихся карточек (количество):{Back.RESET}")
        cursor.execute(
            "select g.Name, g.ID, count(g.ID) Count FROM pMark m inner join Groups g on m.GroupID = g.ID group by g.Name, g.ID;")
        group_for_card_list = []
        for value in cursor:
            group_for_card_list.append(value)
        if len(group_for_card_list) != 0:
            for value in group_for_card_list:
                id = str(value["ID"])
                print(f"{id}: ({value['Count']}) - {value['Name']}")
                cursor.execute(
                    f"select m.ID mID, l.ID lID, Name, FirstName, MidName, TabNumber from pMark m inner join pList l on m.Owner = l.ID where GroupID = {id} order by Name, FirstName, MidName;")
                for value in cursor:
                    mid = str(value["mID"])
                    lid = str(value["lID"])
                    tabNumber = str(value["TabNumber"])
                    lastname = value["Name"]
                    firstname = value["FirstName"]
                    middlename = value["MidName"]
                    print(
                        f"        {Back.GREEN}{tabNumber}/{mid}/{lid}{Back.RESET} {lastname} {firstname} {middlename}")
        else:
            print(f"{Back.RED}Не найдено{Back.RESET}")
        #
        print(f"{Back.RED}Ненужные уровни доступа:{Back.RESET}")
        useless_group_list = []
        connection.commit()
        cursor.execute("select ID, Name from Groups where ID in (select ID from Groups except (select distinct Groups.ID from pMark inner join Groups on pMark.GroupID = Groups.ID)) order by name;")
        for value in cursor:
            useless_group_list.append(value)
        if len(useless_group_list) != 0:
            for value in useless_group_list:
                name = value['Name']
                id = value['ID']
                print(f"{id}: {name}")
        else:
            print(f"{Back.GREEN}Не найдено{Back.RESET}")