from .employee_repository import get_by_login, create_employee, delete_employee
from .equipment_repository import get_by_serial, get_all, update_status, create_equipment, delete_equipment
from .repair_repository import create, get_requests_by_employee, get_requests_by_equipment, delete_by_equipment
from .status_repository import get_all_statuses
from .role_repository import get_all_roles