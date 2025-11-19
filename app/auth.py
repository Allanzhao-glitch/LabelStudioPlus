from flask import Blueprint, request, jsonify
from app.models import User
from app import db
import jwt
from flask import current_app
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

def create_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message':'用户名和密码必填'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message':'用户名或密码错误'}), 401

    token = create_token(user)
    
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username, 'role': user.role}})
