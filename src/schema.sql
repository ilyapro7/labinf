DROP TABLE IF EXISTS repair_requests;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS statuses;

CREATE TABLE statuses (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
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
    FOREIGN KEY (equipment_id) REFERENCES equipment (equipment_id),
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);


INSERT INTO statuses (name) VALUES 
('Свободно'), 
('Выдано'), 
('В ремонте');

INSERT INTO employees (full_name, login, password_hash) VALUES 
('Иванов Иван Иванович', 'Ivanov_ii', 'e150a1ec81e8e93e1eae2c3a77e66ec6dbd6a3b460f89c1d08aecf422ee401a0'), 
('Петров Петр Петрович', 'petrushka_pp', '9bfe77ed73853e942523711df9636ec2c1b42faa1b538cbb4449d1d89194a460');

INSERT INTO equipment (model, serial_number, status_id, employee_id) VALUES 
('Ноутбук Lenovo ThinkPad T14', 'SN-LNV-2026-X1', 2, 1), 
('Монитор Dell UltraSharp U2422H', 'SN-DELL-US-77', 2, 1),  
('Ноутбук ASUS Zenbook 14', 'SN-ASUS-ZB-991', 3, NULL); 