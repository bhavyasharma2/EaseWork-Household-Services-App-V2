from flask import Flask, request, jsonify, session, g, Blueprint
from Code.models import User, Service, ServiceRequest, ServiceType
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from werkzeug.security import generate_password_hash

customer_dashboard_bp = Blueprint('customers', __name__)


def get_db():
    from Code.app import db
    if 'db' not in g:
        g.db = db.session  
    return g.db


@customer_dashboard_bp.route('/customer_home', methods=['GET'])
@jwt_required()
def customer_home():
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    db_user = User.query.filter_by(id=user.get('id')).first()

    if not db_user:
        return jsonify({'error': 'User not found.'}), 404
    
    if db_user.is_blocked:
        return jsonify({
            'message': 'User blocked by admin.',
            'is_blocked': True
        }), 200

    customer_pincode = db_user.pin_code

    return jsonify({
        'message': 'Welcome to your dashboard',
        'is_blocked': db_user.is_blocked,
        'pincode': customer_pincode
    }), 200



@customer_dashboard_bp.route('/customer_edit_profile', methods=['GET', 'POST'])
@jwt_required()
def customer_edit_profile():
    from Code.app import db

    user_data = get_jwt_identity()

    if user_data.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    user = User.query.filter_by(id=user_data.get('id')).first()
    if not user or user.is_blocked:
        return jsonify({'error': 'User not found or blocked'}), 403

    if request.method == 'POST':
        new_email = request.json.get('email')
        new_password = request.json.get('password')
        new_name = request.json.get('full_name')
        new_address = request.json.get('address')
        new_pin_code = request.json.get('pin_code')
        new_mobile_number = request.json.get('mobile_number')

        if new_email and new_email != user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                return jsonify({'error': 'Email already in use'}), 400

        if new_name:
            user.full_name = new_name
        if new_address:
            user.address = new_address
        if new_pin_code:
            user.pin_code = new_pin_code
        if new_mobile_number:
            user.mobile_number = new_mobile_number

        if new_password:
            user.password = generate_password_hash(new_password)

        try:
            db.session.commit()  
            return jsonify({'message': 'Profile updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update profile: {str(e)}'}), 500

    customer_details = {
        'email': user.email,
        'full_name': user.full_name,
        'address': user.address,
        'pin_code': user.pin_code,
        'mobile_number': user.mobile_number
    }
    return jsonify({'customer': customer_details}), 200



@customer_dashboard_bp.route('/available_services', methods=['GET'])
@jwt_required()
def available_services():
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({"error": "Access forbidden: Customers only."}), 403

    services = Service.query.all()
    service_types = ServiceType.query.all()

    services_data = []
    for service in services:
        related_types = [st for st in service_types if st.service_id == service.id]
        services_data.append({
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'time_required': service.time_required,
            'types': [{'id': st.id, 'type_name': st.type_name} for st in related_types]
        })
    
    return jsonify({'services': services_data})  



@customer_dashboard_bp.route('/available_professionals/<int:service_id>', methods=['GET'])
@jwt_required()
def available_professionals(service_id):
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({"error": "Access forbidden: Customers only."}), 403

    db_user = User.query.filter_by(id=user.get('id')).first()

    customer_pincode = db_user.pin_code
    if not customer_pincode:
        return jsonify({"error": "Customer pin code not available."}), 400

    service_type_id = request.args.get('service_type_id')

    query = User.query.filter_by(role='professional', service_id=service_id, pin_code=customer_pincode)

    if service_type_id:
        query = query.filter_by(service_type_id=service_type_id)

    professionals = query.all()

    professionals_data = [{
        'id': professional.id,
        'full_name': professional.full_name,
        'mobile_number': professional.mobile_number,
        'experience': professional.experience,
        'rating': professional.rating
    } for professional in professionals]

    no_professionals = len(professionals) == 0

    return jsonify({'professionals': professionals_data, 'no_professionals': no_professionals})




@customer_dashboard_bp.route('/book_service/<int:professional_id>/<int:service_id>', methods=['POST'])
@jwt_required()
def book_service(professional_id, service_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()
    
    service_type = ServiceType.query.filter_by(service_id=service_id).first()
    if not service_type:
        return jsonify({'error': 'Service type not found'}), 404

    requested_date = request.json.get('requested_date')
    if not requested_date:
        return jsonify({'error': 'Requested date is required'}), 400

    professional = User.query.filter_by(id=professional_id, role='professional').first()
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    
    service_request = ServiceRequest(
        customer_id=customer.id,
        service_id=service_id,
        professional_id=professional_id,
        service_type_id=service_type.id,
        requested_date=requested_date
    )

    db.session.add(service_request)
    db.session.commit()

    return jsonify({'message': 'Service booking confirmed!'})



@customer_dashboard_bp.route('/service_request_history', methods=['GET'])
@jwt_required()
def service_request_history():
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()

    service_requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()

    requests_data = [{
        'id': sr.id,
        'service_id': sr.service_id,
        'professional_name': sr.professional.full_name,
        'service_name': sr.service.name,
        'service_type_id': sr.service_type_id,  
        'status': sr.status,
        'requested_date': sr.requested_date
    } for sr in service_requests]

    return jsonify({
        'service_requests': requests_data,
        'is_blocked': customer.is_blocked  
    })



@customer_dashboard_bp.route('/edit_service_request/<int:request_id>', methods=['PUT'])
@jwt_required()
def edit_service_request(request_id):
    print(f"Received request ID: {request_id}")
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()
    
    new_requested_date = request.json.get('requested_date')
    if not new_requested_date:
        return jsonify({'error': 'New requested date is required'}), 400

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    service_request.requested_date = new_requested_date
    db.session.commit()

    return jsonify({'message': 'Service request updated successfully'})



@customer_dashboard_bp.route('/close_service/<int:request_id>', methods=['POST'])
@jwt_required()
def close_service(request_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()
    
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    service_request.status = 'Completed'
    service_request.completion_date = db.func.current_date()
    db.session.commit()

    return jsonify({'message': 'Service marked as completed', 'service_request_id': service_request.id})



@customer_dashboard_bp.route('/service_review_form/<int:request_id>', methods=['GET'])
@jwt_required()
def service_review_form(request_id):

    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    review_data = {
        'service_request_id': service_request.id,
        'service_name': service_request.service.name,
        'service_type_id': service_request.service_type_id,
        'requested_date': service_request.requested_date,
        'completion_date': service_request.completion_date,
        'professional_name': service_request.professional.full_name,
        'professional_contact': service_request.professional.mobile_number
    }

    return jsonify({'service_request': review_data})



@customer_dashboard_bp.route('/submit_review/<int:request_id>', methods=['POST'])
@jwt_required()
def submit_review(request_id):
    from Code.app import db

    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()

    new_rating = request.json.get('service_rating')
    if not new_rating:
        return jsonify({'error': 'Rating is required'}), 400

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    professional = service_request.professional
    current_rating = professional.rating

    if current_rating is None:
        average_rating = new_rating
    else:
        average_rating = (current_rating + new_rating) / 2

    professional.rating = average_rating
    service_request.status = 'Completed'
    service_request.completion_date = db.func.current_date()
    db.session.commit()

    return jsonify({'message': 'Review submitted successfully', 'average_rating': average_rating})



@customer_dashboard_bp.route('/search_results', methods=['GET'])
@jwt_required()
def search_results():
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403
    
    from Code.app import cache
    
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query cannot be empty'}), 400

    cache_key = f"search_results_{query}"  
    cached_result = cache.get(cache_key)

    if cached_result:
        return jsonify(cached_result)

    
    services = Service.query.filter(Service.name.like(f'%{query}%')).all()
    service_types = ServiceType.query.filter(ServiceType.type_name.like(f'%{query}%')).all()

    
    services_data = [{
        'id': service.id,
        'name': service.name,
        'price': service.price,
        'description': service.description
    } for service in services]

    service_types_data = [{
        'id': st.id,
        'service_id': st.service_id,
        'type_name': st.type_name
    } for st in service_types]

    result = {'services': services_data, 'service_types': service_types_data}

    
    cache.set(cache_key, result, timeout=300)

    
    return jsonify(result)


@customer_dashboard_bp.route('/customer_statistics', methods=['GET'])
@jwt_required()
def customer_statistics():
    user = get_jwt_identity()

    if user.get('role') != 'customer':
        return jsonify({'error': 'Unauthorized access. Customers only.'}), 403

    customer = User.query.filter_by(id=user.get('id')).first()

    total_requests = ServiceRequest.query.filter_by(customer_id=customer.id).count()

    completed_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='Completed').count()

    pending_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='Pending').count()


    statistics = {
        'total_requests': total_requests,
        'completed_requests': completed_requests,
        'pending_requests': pending_requests
    }

    return jsonify({'statistics': statistics})


