from repositories import employee_repository
from repositories import equipment_repository
from services import equipment_service


def admin_menu(user):
    while True:
        print(f"\n МЕНЮ АДМИНИСТРАТОРА ({user})")
        print("1. Посмотреть всё оборудование")
        print("2. Оформить выдачу оборудования")
        print("3. Внести технику в базу")
        print("4. Внести сотрудника в базу")
        print("0. Выйти из аккаунта")

        choice = input("Действие: ")
        if choice == "1":
            print("\nСписок техники:")
            for eq in equipment_repository.get_all():
                print(f"ID: {eq[0]} | {eq[1]} (S/N: {eq[2]}) | Статус: [{eq[5]}]")
        elif choice == "2":
            login = input("Введите логин сотрудника: ")
            sn = input("Введите серийный номер техники: ")
            try:
                equipment_service.hand_out_equipment(login, sn)
                print(" Техника успешно выдана!")
            except Exception as e:
                print(f"X {e}")
        elif choice == "3":
            model = input("Модель техники: ")
            sn = input("Серийный номер: ")
            try:
                equipment_repository.create_equipment(model, sn, 1)  # 1 — Свободно
                print(" Техника успешно внесена в базу!")
            except Exception as e:
                print(f" Ошибка добавления: {e}")
        elif choice == "4":
            name = input("ФИО сотрудника: ")
            login = input("Логин для входа: ")
            pwd = input("Пароль: ")
            try:
                employee_repository.create_employee(name, login, pwd, 2)  # 2 — Сотрудник
                print(" Сотрудник добавлен!")
            except Exception as e:
                print(f" Ошибка добавления: {e}")
        elif choice == "0":
            break


def employee_menu(user):
    while True:
        print(f"\n КАБИНЕТ СОТРУДНИКА ({user})")
        print("1. Просмотреть закрепленное оборудование")
        print("2. Подать заявку на ремонт")
        print("0. Выйти из аккаунта")

        choice = input("Действие: ")
        if choice == "1":
            print("\nВаше оборудование:")
            has_eq = False
            for eq in equipment_repository.get_all():
                if eq[4] == user[0]:
                    print(f"• {eq[1]} (S/N: {eq[2]}) — [{eq[5]}]")
                    has_eq = True
            if not has_eq:
                print("За вами нет закрепленной техники.")
        elif choice == "2":
            sn = input("Введите серийный номер устройства: ")
            defect = input("Описание поломки: ")
            try:
                equipment_service.process_repair_request(sn, user[0], defect)
                print(" Заявка на ремонт оформлена! Статус изменен на 'В ремонте'.")
            except Exception as e:
                print(f"X {e}")
        elif choice == "0":
            break