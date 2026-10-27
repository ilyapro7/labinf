from dataclasses import dataclass
@dataclass
class RepairRequest:
    request_id: int
    equipment_id: int
    employee_id: int
    defect_name: str
