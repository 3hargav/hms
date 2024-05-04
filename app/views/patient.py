from datetime import datetime

from flask import Blueprint, request, jsonify
from app.models import Patient, Doctor, Department, Appointment, MedicalHistory, Availability
from app import db
from app.serializers import *

patient_bp = Blueprint('patient_bp', __name__)


# Patient Routes
@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([patient.serialize() for patient in patients])


@patient_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], contact_info=data['contact_info'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.serialize()), 201


@patient_bp.route('/patients/medical_history', methods=['POST'])
def create_medical_history():
    data = request.json
    patient = Patient.query.get_or_404(data.get('patient_id'))
    if not patient:
        return jsonify({'error': 'Patient is not present in the database'}), 400
    new_medical_history = MedicalHistory(
        patient_id=patient.id,
        previous_diagnoses=data.get('previous_diagnoses'),
        allergies=data.get('allergies'),
        medications=data.get('medications'),
        date_recorded=datetime.utcnow()
    )
    db.session.add(new_medical_history)
    db.session.commit()
    return jsonify(new_medical_history.serialize()), 201


@patient_bp.route('/patients/<int:patient_id>/medical_history', methods=['GET'])
def get_medical_histories(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify([history.serialize() for history in patient.medical_history])


@patient_bp.route('/patients/<int:patient_id>/appointments', methods=['GET'])
def get_patient_appointments(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    return jsonify([appointment.serialize() for appointment in appointments])


# Pagination
@patient_bp.route('/patients/pagination', methods=['GET'])
def paginate_patients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    patients = Patient.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'patients': [patient.serialize() for patient in patients.items],
        'total_pages': patients.pages,
        'total_patients': patients.total
    })
