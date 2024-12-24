from flask import request, jsonify, g, Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from Code.models import User, PendingRegistration, ServiceType, Service

register_bp = Blueprint('register', __name__)



UPLOAD_FOLDER = 'Code/static/uploads/documents'  
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@register_bp.route('/register_professional', methods=['POST'])
def register_professional():
    from Code.app import db
    data = request.form

    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    service_id = data.get('service_id')
    service_type_id = data.get('service_type_id')
    experience = data.get('experience')
    address = data.get('address')
    pin_code = data.get('pin_code')
    mobile_number = data.get('mobile_number')

    if not email or not password or not full_name or not service_id or not service_type_id or not experience or not address or not pin_code or not mobile_number:
        return jsonify({"msg": "All fields are required!"}), 400

    hashed_password = generate_password_hash(password)

    documents_path = None
    if 'documents' in request.files:
        documents_file = request.files['documents']
        if allowed_file(documents_file.filename):
            filename = secure_filename(documents_file.filename)
            documents_path = os.path.join(UPLOAD_FOLDER, filename)
            documents_file.save(documents_path)
        else:
            return jsonify({"msg": "Only PDF files are allowed!"}), 400

    existing_registration = PendingRegistration.query.filter_by(email=email).first()
    if existing_registration:
        return jsonify({"msg": "Email is already registered."}), 400

    pending_registration = PendingRegistration(
        email=email,
        password=hashed_password,
        full_name=full_name,
        address=address,
        pin_code=pin_code,
        mobile_number=mobile_number,
        experience=experience,
        documents_path=documents_path,
        service_id=service_id,
        service_type_id=service_type_id
    )

    try:
        db.session.add(pending_registration)
        db.session.commit()
        return jsonify({"msg": "Registration request has been sent to the admin. Please wait for approval."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500



@register_bp.route('/get_services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{'id': service.id, 'name': service.name} for service in services])



@register_bp.route('/get_service_types/<int:service_id>', methods=['GET'])
def get_service_types(service_id):
    service_types = ServiceType.query.filter_by(service_id=service_id).all()
    return jsonify([{'id': type.id, 'type_name': type.type_name} for type in service_types])



@register_bp.route('/register_customer', methods=['POST'])
def register_customer():
    from Code.app import db
    data = request.json

    #print("Incoming data:", data)  # Log the data # change

    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    address = data.get('address')
    pin_code = data.get('pin_code')
    mobile_number = data.get('mobile_number')


    # Log extracted data
    #print(f"Extracted Data - Email: {email}, Password: {password}, Full Name: {full_name}, "
          #f"Address: {address}, Pin Code: {pin_code}, Mobile Number: {mobile_number}")

     # Change
    #if not all([email, password, full_name, address, pin_code, mobile_number]):
        #return jsonify({"msg": "Missing required fields."}), 400
    

    hashed_password = generate_password_hash(password)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered. Please use a different email."}), 400

    new_user = User(
        email=email,
        password=hashed_password,
        role='customer',  
        full_name=full_name,
        address=address,
        pin_code=pin_code,
        mobile_number=mobile_number,
        rating=0,
        documents_path=None,  
        is_blocked=False
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Customer registered successfully. Please log in."}), 200

