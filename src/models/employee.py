from dataclasses import dataclass
@dataclass
class Employee:
    employee_id: int
    full_name: str
    login: str
    password_hash: str
    userrole: int