from flask import Blueprint, request, jsonify, send_file
from Code.models import User, Service, ServiceType, ServiceRequest, PendingRegistration
from functools import wraps
import jwt
import os
from flask import send_from_directory
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_dashboard_bp = Blueprint('admin', __name__)


@admin_dashboard_bp.route('/admin_home', methods=['GET'])
@jwt_required()
def admin_home():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    return jsonify({"message": "Welcome to the Admin Dashboard"}), 200



@admin_dashboard_bp.route('/new_registration_requests', methods=['GET'])
@jwt_required()
def new_registration_requests():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    registration_requests = PendingRegistration.query.all()
    registration_requests_list = [
        {
            'request_id': request.id,
            'full_name': request.full_name,
            'email': request.email,
            'service_id': request.service_id,
            'service_type_id': request.service_type_id,
            'pin_code': request.pin_code,
            'documents_path': request.documents_path
        }
        for request in registration_requests
    ]
    return jsonify({'registration_requests': registration_requests_list})



@admin_dashboard_bp.route('/view_document/<int:user_id>', methods=['GET'])
@jwt_required()
def view_document(user_id):
    from Code.app import app
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    user = User.query.get(user_id)
    if user and user.documents_path:
        full_path = os.path.join(app.root_path, user.documents_path)
        if os.path.exists(full_path):
            return send_file(full_path)
        return jsonify({"error": "Document not found."}), 404
    return jsonify({"error": "User or document path not found."}), 404



@admin_dashboard_bp.route('/view_document_new_reg/<int:request_id>', methods=['GET'])
@jwt_required()
def view_document_new_reg(request_id):
    from Code.app import app
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    registration = PendingRegistration.query.get(request_id)
    
    if registration and registration.documents_path:
        base_directory = "/home/bhavya/HouseholdServices_MAD2_21f2000707/"
        absolute_path = os.path.join(base_directory, registration.documents_path)

        if os.path.exists(absolute_path):
            return send_file(absolute_path, as_attachment=False, mimetype='application/pdf')
        else:
            return jsonify({"error": "Document not found on the server."}), 404
    return jsonify({"error": "Registration or document path not found."}), 404



@admin_dashboard_bp.route('/approve_registration/<int:request_id>', methods=['POST'])
@jwt_required()
def approve_registration(request_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    registration = PendingRegistration.query.get(request_id)
    if registration:
        new_user = User(
            email=registration.email,
            password=registration.password,
            role='professional',
            full_name=registration.full_name,
            address=registration.address,
            pin_code=registration.pin_code,
            mobile_number=registration.mobile_number,
            experience=registration.experience,
            documents_path=registration.documents_path,
            service_id=registration.service_id,
            service_type_id=registration.service_type_id,
            is_blocked=False
        )
        db.session.add(new_user)
        db.session.delete(registration)
        db.session.commit()
        return jsonify({"message": "Registration approved successfully."}), 200
    return jsonify({"error": "Registration not found."}), 404



@admin_dashboard_bp.route('/reject_registration/<int:request_id>', methods=['POST'])
@jwt_required()
def reject_registration(request_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    registration = PendingRegistration.query.get(request_id)
    if registration:
        db.session.delete(registration)
        db.session.commit()
        return jsonify({"message": "Registration request rejected."}), 200
    return jsonify({"error": "Registration request not found."}), 404



@admin_dashboard_bp.route('/customer_details', methods=['GET'])
@jwt_required()
def customer_details():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    customers = User.query.filter_by(role='customer').all()
    customers_data = [
        {
            "id": customer.id,
            "email": customer.email,
            "full_name": customer.full_name,
            "address": customer.address,
            "pin_code": customer.pin_code,
            "service_request_count": ServiceRequest.query.filter_by(customer_id=customer.id).count(),
            "is_blocked": customer.is_blocked
        }
        for customer in customers
    ]
    return jsonify(customers_data)


# Professional Details
@admin_dashboard_bp.route('/professional_details', methods=['GET'])
@jwt_required()
def professional_details():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    professionals = User.query.filter_by(role='professional').all()
    professionals_data = [
        {
            "id": professional.id,
            "email": professional.email,
            "full_name": professional.full_name,
            "experience": professional.experience,
            "service_name": professional.service.name if professional.service else None,
            "service_type_name": professional.service_type.type_name if professional.service_type else None,
            "address": professional.address,
            "pin_code": professional.pin_code,
            "documents_path": professional.documents_path,
            "service_request_count": ServiceRequest.query.filter_by(professional_id=professional.id).count(),
            "rating": professional.rating,
            "is_blocked": professional.is_blocked
        }
        for professional in professionals
    ]
    return jsonify(professionals_data)



@admin_dashboard_bp.route('/search_professional_by_name', methods=['GET'])
@jwt_required()
def search_professional_by_name():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    query = request.args.get('query')

    professionals = User.query.filter(
        User.role == 'professional',
        User.full_name.ilike(f'%{query}%')
    ).all()

    professionals_list = [
        {
            'id': p.id,
            'email': p.email,
            'full_name': p.full_name,
            'experience': p.experience,
            'service_name': p.service.name if p.service else None,
            'service_type_name': p.service_type.type_name if p.service_type else None,
            'address': p.address,
            'pin_code': p.pin_code,
            'documents_path': p.documents_path,
            'service_request_count': len(p.professional_requests) if p.professional_requests else 0,
            'rating': p.rating,
            'is_blocked': p.is_blocked
        }
        for p in professionals
    ]
    return jsonify({'professionals': professionals_list})



@admin_dashboard_bp.route('/block_user/<int:user_id>', methods=['POST'])
@jwt_required()
def block_user(user_id):
    from Code.app import db
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    user = User.query.get(user_id)
    if user:
        user.is_blocked = True
        db.session.commit()
        return jsonify({"message": "User blocked successfully."}), 200
    return jsonify({"message": "User not found."}), 404



@admin_dashboard_bp.route('/unblock_user/<int:user_id>', methods=['POST'])
@jwt_required()
def unblock_user(user_id):
    from Code.app import db
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    user = User.query.get(user_id)
    if user:
        user.is_blocked = False
        db.session.commit()
        return jsonify({"message": "User unblocked successfully."}), 200
    return jsonify({"message": "User not found."}), 404



@admin_dashboard_bp.route('/service_details', methods=['GET'])
@jwt_required()
def service_details():
    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403
    
    service_id = request.args.get('service_id')
    if service_id:
        service = Service.query.get(service_id)
        if service:
            service_data = {
                'id': service.id,
                'name': service.name,
                'time_required': service.time_required,
                'price': service.price,
                'description': service.description,
                'service_types': [st.type_name for st in service.service_types]
            }
            return jsonify({'service': service_data})
        else:
            return jsonify({'message': 'Service not found.'}), 404

    services = Service.query.all()
    services_list = [
        {
            'id': s.id,
            'name': s.name,
            'time_required': s.time_required,
            'price': s.price,
            'description': s.description,
            'service_types': [st.type_name for st in s.service_types]
        }
        for s in services
    ]
    return jsonify({'services': services_list})


# Edit Service
@admin_dashboard_bp.route('/edit_service/<int:service_id>', methods=['POST'])
@jwt_required()
def edit_service(service_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    service = Service.query.get(service_id)
    if service:
        service_name = request.json.get('service_name')
        time_required = request.json.get('time_required')
        price = request.json.get('price')
        description = request.json.get('description')
        new_service_types = request.json.get('new_service_types', [])

        service.name = service_name
        service.time_required = time_required
        service.price = price
        service.description = description
        db.session.commit()

        for service_type in new_service_types:
            existing_service_type = ServiceType.query.filter_by(type_name=service_type).first()
            if not existing_service_type:
                new_service_type = ServiceType(type_name=service_type, service_id=service.id)
                db.session.add(new_service_type)
        db.session.commit()

        return jsonify({'message': "Service updated successfully."})
    else:
        return jsonify({'message': "Service not found."}), 404



@admin_dashboard_bp.route('/delete_service/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': "Service deleted successfully."})
    else:
        return jsonify({'message': "Service not found."}), 404



@admin_dashboard_bp.route('/add_service', methods=['POST'])
@jwt_required()
def add_service():
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    service_name = request.json.get('service_name')
    time_required = request.json.get('time_required')
    price = request.json.get('price')
    description = request.json.get('description')
    service_types = request.json.get('service_types', [])

    new_service = Service(
        name=service_name,
        time_required=time_required,
        price=price,
        description=description
    )
    db.session.add(new_service)
    db.session.commit()

    for service_type in service_types:
        existing_service_type = ServiceType.query.filter_by(type_name=service_type).first()
        if not existing_service_type:
            new_service_type = ServiceType(type_name=service_type, service_id=new_service.id)
            db.session.add(new_service_type)
    db.session.commit()

    return jsonify({'message': "New service added successfully."})



@admin_dashboard_bp.route('/admin_service_requests', methods=['GET'])
@jwt_required()
def admin_service_requests():

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    service_requests = ServiceRequest.query.all()
    service_requests_list = [
        {
            'id': sr.id,
            'customer_id': sr.customer_id,
            'professional_id': sr.professional_id,
            'service_name': sr.service.name,
            'service_type_id': sr.service_type_id,
            'pin_code': sr.customer.pin_code,
            'status': sr.status,
            'requested_date': sr.requested_date,
            'completion_date': sr.completion_date
        }
        for sr in service_requests
    ]
    return jsonify({'service_requests': service_requests_list})



@admin_dashboard_bp.route('/admin_edit_profile', methods=['POST'])
@jwt_required()
def admin_edit_profile():
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    new_password = request.json.get('new_password')
    user = User.query.get(request.user_id)
    if user and new_password:
        user.password = new_password
        db.session.commit()
        return jsonify({"message": "Password updated successfully."}), 200
    return jsonify({"error": "Invalid data."}), 400



@admin_dashboard_bp.route('/admin_statistics', methods=['GET'])
@jwt_required()
def admin_statistics():
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admins only.'}), 403

    def row_to_dict(row):
        return {column.name: getattr(row, column.name) for column in row.__table__.columns}

    ratings = db.session.query(
        User.rating,
        func.count(User.id).label('count')
    ).filter(User.role == 'professional').group_by(User.rating).all()

    service_requests_by_name = db.session.query(
        Service.name,
        func.count(ServiceRequest.id).label('request_count')
    ).join(ServiceRequest, ServiceRequest.service_id == Service.id).group_by(Service.name).all()

    customers_by_pincode = db.session.query(
        User.pin_code,
        func.count(User.id).label('customer_count')
    ).filter(User.role == 'customer').group_by(User.pin_code).all()

    service_requests_by_status = db.session.query(
        ServiceRequest.status,
        func.count(ServiceRequest.id).label('request_count')
    ).group_by(ServiceRequest.status).all()

    ratings_list = [{"rating": row[0], "count": row[1]} for row in ratings]
    service_requests_by_name_list = [{"name": row[0], "request_count": row[1]} for row in service_requests_by_name]
    customers_by_pincode_list = [{"pin_code": row[0], "customer_count": row[1]} for row in customers_by_pincode]
    service_requests_by_status_list = [{"status": row[0], "request_count": row[1]} for row in service_requests_by_status]

    return jsonify({
        "professional_ratings": ratings_list,
        "service_requests_by_name": service_requests_by_name_list,
        "customers_by_pincode": customers_by_pincode_list,
        "service_requests_by_status": service_requests_by_status_list
    })





