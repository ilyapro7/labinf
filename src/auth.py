from repositories import employee_repository

def authenticate(login: str, password_raw: str):
    employee = employee_repository.get_by_login(login)
    if employee and employee[3] == password_raw:  # employee[3] — это password_hash
        return employee
    return None