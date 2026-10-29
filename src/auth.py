import hashlib
from repositories import employee_repository


def authenticate(login: str, password_raw: str):
    employee = employee_repository.get_by_login(login)

    password_hash = hashlib.sha256(password_raw.encode('utf-8')).hexdigest()

    if employee and employee[3] == password_hash:
        return employee
    return None