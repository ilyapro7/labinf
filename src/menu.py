from repositories import employee_repository
from repositories import equipment_repository
from repositories import repair_repository
from services import equipment_service


def admin_menu(user):
    while True:
        print(f"\nМЕНЮ АДМИНИСТРАТОРА ({user[1]})")
        print("1. Посмотреть все оборудование")
        print("2. Оформить выдачу оборудования")
        print("3. Внести технику в базу")
        print("4. Внести сотрудника в базу")
        print("5. Посмотреть список сотрудников")
        print("6. Удалить сотрудника")
        print("7. Удалить технику из базы")
        print("0. Выйти из аккаунта")

        choice = input("Действие: ")

        if choice == "1":
            print("\nСписок техники:")
            for eq in equipment_repository.get_all():

                status_text = eq[5]
                extra_info = f"Статус: [{status_text}]"


                if status_text == "В ремонте":
                    reqs = repair_repository.get_requests_by_equipment(eq[0])
                    if reqs:
                        defect = reqs[-1][2]  # текст поломки
                        extra_info += f" | Поломка: {defect}"

                print(f"ID: {eq[0]} | Модель: {eq[1]} | S/N: {eq[2]} | {extra_info}")

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
                equipment_repository.create_equipment(model, sn, 1)
                print(" Техника успешно внесена в базу!")
            except Exception as e:
                print(f" Ошибка добавления: {e}")

        elif choice == "4":
            name = input("ФИО сотрудника: ")
            login = input("Логин для входа: ")
            pwd = input("Пароль: ")
            try:
                employee_repository.create_employee(name, login, pwd, 2)
                print(" Сотрудник добавлен!")
            except Exception as e:
                print(f" Ошибка добавления: {e}")

        elif choice == "5":
            print("\nСписок сотрудников:")
            employees = employee_repository.get_all_employees()
            for emp in employees:

                role_name = "Администратор" if emp[3] == 1 else "Сотрудник"
                print(f"ID: {emp[0]} | ФИО: {emp[1]} | Логин: {emp[2]} | Роль: {role_name}")

        elif choice == "6":
            login_to_delete = input("Введите логин сотрудника для удаления: ").strip()
            try:
                emp = employee_repository.get_by_login(login_to_delete)
                if not emp:
                    raise Exception("Сотрудник с таким логином не найден!")

                emp_id = emp[0]
                all_eq = equipment_repository.get_all()
                has_equipment = any(str(eq[4]) == str(emp_id) for eq in all_eq)

                if has_equipment:
                    raise Exception("Нельзя удалить сотрудника, за которым закреплено оборудование!")

                employee_repository.delete_employee_by_login(login_to_delete)
                print(f"Сотрудник '{login_to_delete}' успешно удален!")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

        elif choice == "7":
            serial_num = input("Введите серийный номер техники для удаления: ").strip()
            try:
                eq = equipment_repository.get_by_serial(serial_num)
                if not eq:
                    raise Exception("Техника с таким серийным номером не найдена!")


                if eq[3] in (2, 3):
                    raise Exception(
                        f"Нельзя удалить технику, так как она у сотрудника или в ремонте (Статус ID: {eq[3]})")

                equipment_repository.delete_equipment(eq[0])
                print("Техника успешно удалена из базы!")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

        elif choice == "0":
            break



def employee_menu(user):
    while True:
        print(f"\n КАБИНЕТ СОТРУДНИКА ({user[1]}) ")
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