from dataclasses import dataclass
@dataclass
class Equipment:
    equipment_id: int
    model: str
    serial_number: str
    status_id: int
    employee_id: int | None = None


    status_name: str | None = None