from app.models import Patient, Doctor, Department, Appointment, MedicalHistory, Availability


def serialize_patient(patient):
    return {
        'id': patient.id,
        'name': patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'contact_info': patient.contact_info,
        'medical_histories': [serialize_medical_history(history) for history in patient.medical_history]
    }


def serialize_medical_history(medical_history):
    return {
        'id': medical_history.id,
        'patient_id': medical_history.patient_id,
        'previous_diagnoses': medical_history.previous_diagnoses,
        'allergies': medical_history.allergies,
        'medications': medical_history.medications,
        'date_recorded': medical_history.date_recorded.strftime('%Y-%m-%d %H:%M:%S')
    }


def serialize_doctor(doctor):
    return {
        'id': doctor.id,
        'name': doctor.name,
        'specialization': doctor.specialization,
        'contact_info': doctor.contact_info,
        'department_id': doctor.department_id
    }


def serialize_availability(availability):
    return {
        'doctor_id': availability.doctor_id,
        'day_of_week': availability.day_of_week,
        'start_time': availability.start_time,
        'end_time': availability.end_time
    }


def serialize_department(department):
    return {
        'id': department.id,
        'name': department.name,
        'services_offered': department.services_offered
    }


def serialize_appointment(appointment):
    return {
        'id': appointment.id,
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'start_time': appointment.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': appointment.end_time.strftime('%Y-%m-%d %H:%M:%S')
    }


# Serialization for related models
Patient.serialize = serialize_patient
MedicalHistory.serialize = serialize_medical_history
Doctor.serialize = serialize_doctor
Availability.serialize = serialize_availability
Department.serialize = serialize_department
Appointment.serialize = serialize_appointment
