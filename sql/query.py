AUTH_USER = """
SELECT count(*) FROM user WHERE username = '%s' AND password = '%s'
"""

GET_SPECIALIZATION = """
SELECT id, value FROM specialization ORDER BY value
"""

ADD_DOCTOR = """
INSERT INTO doctor(surname, name, patronymic, b_date) VALUES ('%s', '%s', '%s', '%s')
"""

UPDATE_DOCTOR = """
UPDATE doctor set surname = '%s', name = '%s', patronymic = '%s', b_date = '%s' WHERE id = '%s'
"""

UPDATE_SPECIALIST = """
INSERT INTO specialist(spec_code, doctor_id, category_name, cabinet_id)
VALUES ('%s', '%s', '%s', (SELECT cabinet_number FROM cabinet_assign WHERE specialization_id = '%s'))
"""

ADD_SPECIALIST = """
INSERT INTO specialist(spec_code, doctor_id, category_name) VALUES ('%s', '%s', '%s')
"""
ADD_PATIENT = """
INSERT INTO patient(surname, name, b_date, gender, doc_s, doc_num) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
"""

SPECIALIST_LIST = """
SELECT d.id, d.surname || ' ' || substr(d.name, 1, 1) || '.' || substr(d.patronymic, 1, 1) || '.' || ', ' || s2.value
FROM doctor d
INNER JOIN specialist s on d.id = s.doctor_id
INNER JOIN specialization s2 ON s2.id = s.spec_code
"""

SEARCH_PATIENT = """
SELECT p.id, p.surname || ' ' || substr(p.name, 1, 1) || '.' || ifnull(substr(p.patronymic, 1, 1), '')  || ', ' || b_date as details FROM patient p WHERE p.surname = '%s';
"""

INSERT_AP_RECORD = """
INSERT INTO appointment(patient_id, specialist_id, visit_date) VALUES ('%s', '%s', '%s')
"""