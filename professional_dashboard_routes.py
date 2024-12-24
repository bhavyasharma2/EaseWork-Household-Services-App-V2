from flask import Blueprint, request, jsonify, session, redirect, url_for
from Code.models import User, ServiceRequest
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash
from io import StringIO
import csv
from datetime import datetime

professional_dashboard_bp = Blueprint('professional', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@professional_dashboard_bp.route('/professional_home', methods=['GET'])
@jwt_required()
def professional_home():
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    is_blocked = professional.is_blocked
    return jsonify({'is_blocked': is_blocked})



@professional_dashboard_bp.route('/prof_edit_profile', methods=['GET', 'POST'])
@jwt_required()
def prof_edit_profile():
    from Code.app import db, app
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'POST':
        data = request.form
        full_name = data.get('full_name', professional.full_name)
        password = data.get('password', None)
        experience = data.get('experience', professional.experience)
        address = data.get('address', professional.address)
        pin_code = data.get('pin_code', professional.pin_code)
        mobile_number = data.get('mobile_number', professional.mobile_number)
        documents = request.files.get('documents')

        documents_path = professional.documents_path
        if documents:
            if allowed_file(documents.filename):
                filename = secure_filename(documents.filename)
                documents_path = os.path.join("static/uploads/documents", filename)
                documents.save(os.path.join(app.root_path, documents_path))
            else:
                return jsonify({'message': 'Only PDF files are allowed.'}), 400

        if password:
            hashed_password = generate_password_hash(password)
            professional.password = hashed_password

        professional.full_name = full_name
        professional.experience = experience
        professional.address = address
        professional.pin_code = pin_code
        professional.mobile_number = mobile_number
        professional.documents_path = documents_path

        try:
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

    return jsonify({
        'full_name': professional.full_name,
        'experience': professional.experience,
        'address': professional.address,
        'pin_code': professional.pin_code,
        'mobile_number': professional.mobile_number,
        'documents_path': professional.documents_path
    })



@professional_dashboard_bp.route('/prof_service_requests', methods=['GET'])
@jwt_required()
def prof_service_requests():
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    pending_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='Pending').all()
    assigned_rejected_requests = ServiceRequest.query.filter(ServiceRequest.professional_id == professional.id, ServiceRequest.status.in_(['Assigned', 'Rejected'])).all()
    closed_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='Completed').all()

    is_blocked = professional.is_blocked

    return jsonify({
        'pending_requests': [{'id': req.id, 'customer_name': req.customer.full_name, 'requested_date': req.requested_date} for req in pending_requests],
        'assigned_rejected_requests': [{'id': req.id, 'customer_name': req.customer.full_name, 'status': req.status, 'requested_date': req.requested_date} for req in assigned_rejected_requests],
        'closed_requests': [{'id': req.id, 'customer_name': req.customer.full_name, 'status': req.status, 'requested_date': req.requested_date, 'completion_date': req.completion_date} for req in closed_requests],
        'is_blocked': is_blocked
    })



@professional_dashboard_bp.route('/accept_request/<int:request_id>', methods=['GET'])
@jwt_required()
def accept_request(request_id):
    from Code.app import db
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=professional.id).first()
    if service_request:
        service_request.status = 'Assigned'
        db.session.commit()
        return jsonify({'message': 'Request accepted successfully'})

    return jsonify({'error': 'Request not found or already processed'}), 404



@professional_dashboard_bp.route('/reject_request/<int:request_id>', methods=['GET'])
@jwt_required()
def reject_request(request_id):
    from Code.app import db
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=professional.id).first()
    if service_request:
        service_request.status = 'Rejected'
        db.session.commit()
        return jsonify({'message': 'Request rejected successfully'})

    return jsonify({'error': 'Request not found or already processed'}), 404



@professional_dashboard_bp.route('/professional_statistics', methods=['GET'])
@jwt_required()
def professional_statistics():
    from Code.app import db
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'message': 'Access forbidden: Professionals only.'}), 403

    professional = User.query.filter_by(id=user.get('id')).first()
    if not professional:
        return jsonify({'error': 'User not found'}), 404

    professional_rating = professional.rating or 'No rating available'

    stats = db.session.query(ServiceRequest.status, db.func.count().label('count')) \
        .filter(ServiceRequest.professional_id == professional.id) \
        .group_by(ServiceRequest.status).all()

    service_requests_by_status = [{'status': status, 'count': count} for status, count in stats]

    return jsonify({
        'professional_rating': professional_rating,
        'service_requests_by_status': service_requests_by_status
    })


@professional_dashboard_bp.route('/export_csv', methods=['POST'])
@jwt_required()
def export_csv():
    user = get_jwt_identity()

    if user.get('role') != 'professional':
        return jsonify({'error': 'Unauthorized access'}), 403

    professional_id = user.get('id')

    all_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()

    if not all_requests:
        return jsonify({'message': 'No service requests found.'}), 404

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Request ID', 'Service Name', 'Customer Name', 'Status'])  

    for request in all_requests:
        customer = User.query.get(request.customer_id)  

        writer.writerow([
            request.id, 
            request.service.name, 
            customer.full_name, 
            request.status  
        ])

    
    output.seek(0)  
    csv_content = output.getvalue()


    response = jsonify({'message': 'CSV export completed successfully.'})
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=exported_requests.csv'
    response.set_data(csv_content)  

    return response


