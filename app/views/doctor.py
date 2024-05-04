from datetime import datetime

from flask import Blueprint, request, jsonify
from app.models import Doctor, Department, Appointment, Availability
from app import db
from app.serializers import *
doc_bp = Blueprint('doc_bp', __name__)


# Doctor Routes
@doc_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        return jsonify(doctor.serialize())
    else:
        return jsonify({'error': 'Doctor not found'}), 400


@doc_bp.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    name = data.get('name')
    specialization = data.get('specialization')
    contact_info = data.get('contact_info')
    department_id = data.get('department_id')

    new_doctor = Doctor(name=name, specialization=specialization, contact_info=contact_info)

    if department_id:
        department = Department.query.get(department_id)
        if not department:
            return jsonify({'error': 'Department not found, Please provide available one'}), 400
        new_doctor.department = department.id

    db.session.add(new_doctor)
    db.session.commit()

    return jsonify(new_doctor.serialize()), 201


@doc_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.json

    name = data.get('name', doctor.name)
    specialization = data.get('specialization', doctor.specialization)
    contact_info = data.get('contact_info', doctor.contact_info)
    department_id = data.get('department_id', doctor.department_id)

    if department_id:
        department = Department.query.get_or_404(department_id)
        doctor.department_id = department.id

    doctor.name = name
    doctor.specialization = specialization
    doctor.contact_info = contact_info

    db.session.commit()

    return jsonify(doctor.serialize())


@doc_bp.route('/doctors/<int:doctor_id>/availability', methods=['POST'])
def create_availability(doctor_id):
    data = request.json
    dow: str = data.get('day_of_week')
    doctor = Doctor.query.get_or_404(doctor_id)
    new_availability = Availability(doctor_id=doctor_id,
                                    day_of_week=dow.lower(),
                                    start_time=data.get('start_time'),
                                    end_time=data.get('end_time'))
    db.session.add(new_availability)
    db.session.commit()
    return jsonify(new_availability.serialize()), 201


@doc_bp.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_doctor_availability(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    availability = Availability.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([av.serialize() for av in availability])


@doc_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not doctor_id or not start_time or not end_time:
        return jsonify({'error': 'Doctor ID, Start Time, and End Time are required'}), 400

    doctor = Doctor.query.get_or_404(doctor_id)

    start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    # Check if the doctor is available
    availability = Availability.query.filter_by(doctor_id=doctor_id,
                                                day_of_week=start_time_obj.strftime('%A').lower()).first()
    if not availability:
        return jsonify({'error': 'Doctor is not available on the specified day'}), 400

    # Check if the appointment duration is within the doctor's availability
    print(datetime.strptime(availability.start_time, '%H:%M').time())
    print(datetime.strptime(availability.end_time, '%H:%M').time())
    if start_time_obj.time() < datetime.strptime(availability.start_time, '%H:%M').time() or \
            end_time_obj.time() > datetime.strptime(availability.end_time, '%H:%M').time():
        return jsonify({'error': 'Appointment time is not within doctor\'s availability'}), 400

    # Check if there's no overlapping appointment
    overlapping_appointment = Appointment.query.filter_by(doctor_id=doctor_id).filter(
        (Appointment.start_time <= end_time_obj) & (Appointment.end_time >= start_time_obj)).first()
    if overlapping_appointment:
        return jsonify({'error': 'Appointment time overlaps with existing appointment'}), 400

    new_appointment = Appointment(patient_id=data['patient_id'],
                                  doctor_id=doctor_id,
                                  start_time=start_time_obj,
                                  end_time=end_time_obj)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.serialize()), 201


@doc_bp.route('/doctors/<int:doctor_id>/appointments', methods=['GET'])
def get_doctor_appointments(doctor_id):
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({'error': 'Start Time and End Time are required'}), 400

    doctor = Doctor.query.get_or_404(doctor_id)

    appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(
        Appointment.start_time.between(start_time, end_time),
        Appointment.end_time.between(start_time, end_time)
    ).all()

    return jsonify([appointment.serialize() for appointment in appointments])
