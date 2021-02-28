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