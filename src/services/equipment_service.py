from repositories import employee_repository
from repositories import equipment_repository
from repositories import repair_repository

def process_repair_request(serial_number: str, employee_id: int, defect_name: str):
    """Обработка заявки на ремонт"""
    while True:
        eq = equipment_repository.get_by_serial(serial_number)
        if eq is not None:
            break
        else:
            raise Exception("Номер устройства неверный! Повторите ввод.")


    equipment_repository.update_status(eq[0], 3, None)

    repair_repository.create(eq[0], employee_id, defect_name)


def hand_out_equipment(employee_login: str, serial_number: str):
    """Оформление выдачи оборудования"""
    emp =employee_repository.get_by_login(employee_login)
    if emp is None:
        raise Exception("Сотрудник не найден в базе!")

    eq = equipment_repository.get_by_serial(serial_number)
    if eq is None:
        raise Exception("Техника с таким номером не найдена!")

    if eq[3] != 1:
        raise Exception(f"Техника занята или в ремонте! Текущий статус ID: {eq[5]}")


    equipment_repository.update_status(eq[0], 2, emp[0])