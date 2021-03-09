AUTH_USER = """
SELECT count(*) FROM user WHERE username = %s AND password = %s
"""

GET_SPECIALIZATION = """
SELECT id, value FROM specialization ORDER BY value
"""

ADD_DOCTOR = """
INSERT INTO doctor(surname, name, patronymic, b_date) VALUES (%s, %s, %s, %s)
"""

UPDATE_DOCTOR = """
UPDATE doctor set surname = %s, name = %s, patronymic = %s, b_date = %s WHERE id = %s
"""

ADD_SPECIALIST = """
INSERT INTO specialist(spec_code, doctor_id, category_name) VALUES (%s, %s, %s)
"""

ADD_PATIENT = """
INSERT INTO patient(surname, name, patronymic, b_date, gender, doc_s, doc_num) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_PATIENT = """
UPDATE patient SET surname = %s, name=%s, patronymic=%s, b_date = %s, gender = %s, doc_s = %s, doc_num = %s WHERE id = %s
"""

GET_PATIENT = """
SELECT surname, name, patronymic, b_date, gender, doc_s, doc_num FROM patient WHERE id = %s
"""

GET_PATIENT_CONTACTS = """
SELECT pc.number, t.value FROM patient_contact pc 
INNER JOIN tel_type t ON 
pc.tel_type_id = t.id
WHERE pc.patient_id = %s
"""

SPECIALIST_LIST = """
SELECT d.id, CONCAT(d.surname, ' ', substr(d.name, 1, 1), '.', substr(d.patronymic, 1, 1), ', ', s2.value) AS fullname
FROM doctor d
INNER JOIN specialist s on d.id = s.doctor_id
INNER JOIN specialization s2 ON s2.id = s.spec_code
"""

SEARCH_PATIENT = """
SELECT p.id, CONCAT(p.surname,' ', substr(p.name, 1, 1), '.', ifnull(substr(p.patronymic, 1, 1), ''), ', ', b_date) as details 
FROM patient p WHERE p.surname LIKE '%s%%'
"""

INSERT_AP_RECORD = """
INSERT INTO appointment(patient_id, specialist_id, visit_date, number_ticket) VALUES (%(patient_idx)s, %(specialist_idx)s, %(visit_date)s, %(ticket_id)s)
"""

GET_TEL_TYPES = """
SELECT id, value FROM tel_type
"""
GET_PATIENT_LIST = """
SELECT p.id, CONCAT(p.surname, ' ', substr(p.name, 1, 1),'.',ifnull(substr(p.patronymic, 1, 1), '')) as details, b_date,
doc_s, doc_num FROM patient p
"""

INSERT_CONTACTS = """
INSERT INTO patient_contact(number, tel_type_id, patient_id) VALUES(%s, %s, %s)
"""

GET_APPOINTMENTS = """
SELECT a.id, visit_date, CONCAT(p.surname, ' ', p.name, ' ' , p.patronymic, ' ', p.b_date) as patient,
       CONCAT(d.surname, ' ', SUBSTR(d.name, 1, 1), '.', SUBSTR(d.patronymic, 1, 1), '.', ' ', s.value) as doc
FROM appointment a
INNER JOIN patient p on a.patient_id = p.id
INNER JOIN specialization s on a.specialist_id = s.id
INNER JOIN specialist s2 on a.specialist_id = s2.id
INNER JOIN doctor d on s2.doctor_id = d.id
"""

DEL_APPOINTMENTS = """
DELETE FROM appointment WHERE id = %s
"""

LATEST_TICKET = """
SELECT IFNULL(max(number_ticket), 0) + 1 lticket FROM appointment WHERE visit_date = CURRENT_DATE
"""

TICKET_CONTEXT = """
SELECT a.number_ticket talon_number, CONCAT(p.surname, ' ', p.name, ' ', p.patronymic, ' ',
    DATE_FORMAT(p.b_date, '%Y'), ' г.р.') fullname_patient, DATE_FORMAT(a.visit_date, '%d-%m-%Y') visit_date_,
       CONCAT(d.surname, ' ', d.name, ' ', d.patronymic) fullname_doctor, c.number cab_num FROM appointment a
JOIN patient p on p.id = a.patient_id
JOIN specialist s on s.id = a.specialist_id
JOIN doctor d on d.id = s.doctor_id
JOIN cabinet c on s.id = c.spec_id
WHERE a.id = %s"""