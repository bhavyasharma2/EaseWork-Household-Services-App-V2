from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from Code.models import User
from flask_jwt_extended import create_access_token, jwt_required

login_and_logout_bp = Blueprint('auth', __name__)


@login_and_logout_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required!"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User not found. Please register first."}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid password. Try again."}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})

    return jsonify({'token': access_token, 'role': user.role}), 200



@login_and_logout_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logged out successfully."}), 200


