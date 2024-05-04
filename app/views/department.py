from flask import Blueprint, request, jsonify
from app import db
from app.serializers import *

department_bp = Blueprint('department_bp', __name__)


@department_bp.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([department.serialize() for department in departments])


@department_bp.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    new_department = Department(name=data['name'], services_offered=data['services_offered'])
    db.session.add(new_department)
    db.session.commit()
    return jsonify(new_department.serialize()), 201


@department_bp.route('/departments/<int:department_id>', methods=['GET'])
def get_department_id(department_id):
    department = Department.query.get(department_id)
    if department:
        return jsonify(department.serialize())
    else:
        return jsonify({'error': 'Department not found'}), 400


@department_bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('type')
    query = request.args.get('query')

    if not search_type or not query:
        return jsonify({'error': 'Please provide both type and query parameters'}), 400

    if search_type == 'patient':
        patients = Patient.query.filter(Patient.name.ilike(f'%{query}%')).all()
        return jsonify([patient.serialize() for patient in patients])

    elif search_type == 'doctor':
        doctors = Doctor.query.filter(Doctor.name.ilike(f'%{query}%')).all()
        return jsonify([doctor.serialize() for doctor in doctors])

    elif search_type == 'department':
        departments = Department.query.filter(Department.name.ilike(f'%{query}%')).all()
        return jsonify([department.serialize() for department in departments])

    else:
        return jsonify({'error': 'Invalid search type'}), 400


@department_bp.route('/filter', methods=['GET'])
def filter_case():
    filter_type = request.args.get('type')
    filter_value = request.args.get('value')

    if not filter_type or not filter_value:
        return jsonify({'error': 'Please provide both type and value parameters'}), 400

    if filter_type == 'availability':
        available_doctors = Availability.query.filter(Availability.day_of_week.ilike(f'%{filter_value}%')).all()
        return jsonify([availability.doctor.serialize() for availability in available_doctors])

    elif filter_type == 'specialization':
        specialized_doctors = Doctor.query.filter(Doctor.specialization.ilike(f'%{filter_value}%')).all()
        return jsonify([doctor.serialize() for doctor in specialized_doctors])

    else:
        return jsonify({'error': 'Invalid filter type'}), 400
