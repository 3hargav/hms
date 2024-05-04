
#### Create Patients 
```bash
curl --location 'http://127.0.0.1:5000/api/patients' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Bhargav",
    "age": 25,
    "gender": "male",
    "contact_info": "+918309676523"
}'
```
Response
```bash
{
    "age": 25,
    "contact_info": "+918309676523",
    "gender": "male",
    "id": 2,
    "medical_histories": [],
    "name": "Chaitanya"
}
```
####  POST medical history for a patient 
```bash
curl --location 'http://127.0.0.1:5000/api/patients/medical_history' \
--header 'Content-Type: application/json' \
--data '{
    "patient_id": 1,
    "previous_diagnoses": "diabetes",
    "allergies": "nut",
    "medications":"aspirin"
}'
```
Response
```bash

{
    "allergies": "nut",
    "date_recorded": "2024-05-04 08:34:41",
    "id": 1,
    "medications": "aspirin",
    "patient_id": 1,
    "previous_diagnoses": "diabetes"
}
```
####  GET medical history for a patient 
```bash
http://127.0.0.1:5000/api/patients/1/medical_histories
```
####  GET patients via pagination 
```bash
http://127.0.0.1:5000/api/patients/pagination
```
Response
```bash
{
    "patients": [
        {
            "age": 25,
            "contact_info": "+918309676523",
            "gender": "male",
            "id": 1,
            "medical_histories": [
                {
                    "allergies": "nut",
                    "date_recorded": "2024-05-04 08:34:41",
                    "id": 1,
                    "medications": "aspirin",
                    "patient_id": 1,
                    "previous_diagnoses": "diabetes"
                }
            ],
            "name": "Bhargav"
        },
        {
            "age": 25,
            "contact_info": "+918309676523",
            "gender": "male",
            "id": 2,
            "medical_histories": [],
            "name": "Chaitanya"
        }
    ],
    "total_pages": 1,
    "total_patients": 2
}
```
####  POST doctors
```bash
curl --location 'http://127.0.0.1:5000/api/doctors' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Chaitanya",
    "specialization": "cardiaology",
    "contact_info": "83096765232"
    }'
```
Response
```bash

{
    "contact_info": "83096765232",
    "department_id": null,
    "id": 6,
    "name": "Sumanth",
    "specialization": "cardiology"
}
```
####  GET doctor by id
```bash
http://127.0.0.1:5000/api/doctors/3
```
####  POST doctor's availability schedule

```bash
curl --location 'http://127.0.0.1:5000/api/doctors/1/availability' \
--header 'Content-Type: application/json' \
--data '{
    "day_of_week": "tuesday",
    "start_time": "09:00",
    "end_time": "03:00"
    }'
 ```
####  GET doctor's availability schedule with doctor_id
```bash
http://127.0.0.1:5000/api/doctors/1/availability
```
####  POST departments
```bash
curl --location 'http://127.0.0.1:5000/api/departments' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Anatomy",
    "services_offered": "Bone Replacement, knee surgery"
}'
```
Response
```bash
{
    "id": 2,
    "name": "Anatomy",
    "services_offered": "Bone Replacement, knee surgery"
}
```
####  UPDATE department for doctor
```bash
curl --location --request PUT 'http://127.0.0.1:5000/api/doctors/6' \
--header 'Content-Type: application/json' \
--data '{
    "department_id": 2,
    "specialization": "cardiology"
}'
```
Response
```bash
{
    "contact_info": "83096765232",
    "department_id": 2,
    "id": 6,
    "name": "Sumanth",
    "specialization": "cardiology"
}
```

####  Create appointment between doctor and patient for given time
```bash

curl --location 'http://127.0.0.1:5000/api/appointments' \
--header 'Content-Type: application/json' \
--data '{
    "doctor_id": 6,
    "patient_id": 1,
    "start_time": "2024-05-06 10:00:00",
    "end_time": "2024-05-06 11:00:00"
}'
```
Response
```bash
{
    "doctor_id": 6,
    "end_time": "2024-05-06 11:00:00",
    "id": 2,
    "patient_id": 1,
    "start_time": "2024-05-06 10:00:00"
}
```
####  GET doctor's appointments
```bash
curl --location 'http://127.0.0.1:5000/api/doctors/6/appointments?start_time=2024-05-06%2010%3A00%3A00&end_time=2024-05-06%2011%3A00%3A00'
```
####  GET patient's appointments
```bash
curl --location 'http://127.0.0.1:5000/api/patients/1/appointments'
```

####  GET doctor's availability schedule

```bash
curl --location 'http://127.0.0.1:5000/api/doctors/6/availability'
```
Response
```bash
[
    {
        "day_of_week": "tuesday",
        "doctor_id": 6,
        "end_time": "17:00",
        "start_time": "09:00"
    },
    {
        "day_of_week": "monday",
        "doctor_id": 6,
        "end_time": "12:00",
        "start_time": "09:00"
    }
]
```

####  Search for doctors, patients, departments
```bash
curl --location 'http://127.0.0.1:5000/api/search?type=doctor&query=sumanth'
```
Response
```bash
[
    {
        "contact_info": "83096765232",
        "department_id": 2,
        "id": 6,
        "name": "Sumanth",
        "specialization": "cardiology"
    }
]

```
####  Filter by specialization, availability
```bash
curl --location 'http://127.0.0.1:5000/api/filter?type=specialization&value=cardiology'
```
Response
```bash
[
    {
        "contact_info": "83096765232",
        "department_id": 2,
        "id": 6,
        "name": "Sumanth",
        "specialization": "cardiology"
    }
]
```
