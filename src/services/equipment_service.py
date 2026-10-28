from repositories import employee_repository
from repositories import equipment_repository
from repositories import repair_repository

def process_repair_request(serial_number: str, employee_id: int, defect_name: str):
    """Обработка заявки на ремонт"""
    while True:
        eq = equipment_repository.get_by_serial(serial_number)
        if eq is not None:
            break  # Проверка верности номера устройства
        else:
            raise Exception("Номер устройства неверный! Повторите ввод.")

    # Перевод в статус "В ремонте" и открепление от сотрудника
    equipment_repository.update_status(eq[0], 3, None)
    # Создание заявки в repair_requests
    repair_repository.create(eq[0], employee_id, defect_name)


def hand_out_equipment(employee_login: str, serial_number: str):
    """Оформление выдачи оборудования"""
    emp =employee_repository.get_by_login(employee_login)
    if emp is None:
        raise Exception("Сотрудник не найден в базе!")

    eq = equipment_repository.get_by_serial(serial_number)
    if eq is None:
        raise Exception("Техника с таким номером не найдена!")

    if eq[3] != 1:  # eq[3] — это status_id в кортеже. 1 — Свободно
        raise Exception(f"Техника занята или в ремонте! Текущий статус ID: {eq[3]}")

    # Закрепить устройство за сотрудником и сменить статус на "Занято"
    equipment_repository.update_status(eq[0], 2, emp[0])