DROP TABLE IF EXISTS repair_requests;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS roles;

CREATE TABLE statuses (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE roles (
    userrole INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE

);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    userrole INTEGER NOT NULL,
    FOREIGN KEY (userrole) REFERENCES roles (userrole)
);


CREATE TABLE equipment (
    equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    serial_number TEXT NOT NULL UNIQUE,
    status_id INTEGER NOT NULL,
    employee_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES statuses (status_id),
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);


CREATE TABLE repair_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    defect_name TEXT NOT NULL,
    FOREIGN KEY (equipment_id) REFERENCES equipment (equipment_id),
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);



INSERT INTO statuses (name) VALUES 
('Свободно'), 
('Выдано'), 
('В ремонте');

INSERT INTO roles (userrole, name) VALUES
(1, 'admin'),
(2, 'employee');

INSERT INTO employees (full_name, login, password_hash, userrole) VALUES
('Иванов Иван Иванович', 'Ivanov_ii', 'admin', 1),
('Петров Петр Петрович', 'petrushka_pp', '12345', 2);

INSERT INTO equipment (model, serial_number, status_id, employee_id) VALUES 
('Ноутбук Lenovo ThinkPad T14', 'SN-LNV-2026-X1', 2, 2),
('Монитор Dell UltraSharp U2422H', 'SN-DELL-US-77', 2, 2),
('Ноутбук ASUS Zenbook 14', 'SN-ASUS-ZB-991', 3, NULL);



