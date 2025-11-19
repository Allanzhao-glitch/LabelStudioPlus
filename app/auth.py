from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# ① GET 显示登录界面（访问 http://localhost:5000/login）
@auth_bp.route('/login', methods=['GET'])
def login_page():
    # 如果已经登录，则重定向到对应主页
    if 'user_id' in session:
        user_role = session.get('user_role')
        print(f"User already logged in with role: {user_role}")  # 调试信息
        if user_role == 'admin':
            return redirect('/admin')
        elif user_role == 'annotator':
            return redirect('/annotator')
    return render_template("login.html")

# 添加 POST 方法处理登录请求
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"msg": "用户名和密码不能为空"}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # 设置session
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role
            
            print(f"User {username} logged in with role {user.role}")  # 调试信息
            
            # 根据角色确定重定向URL
            redirect_url = '/'
            if user.role == 'admin':
                redirect_url = '/admin'
            elif user.role == 'annotator':
                redirect_url = '/annotator'
            
            # 返回JSON响应
            return jsonify({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role
                },
                'redirect_url': redirect_url
            }), 200
        else:
            return jsonify({"msg": "用户名或密码错误"}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")  # 调试信息
        return jsonify({"msg": "登录失败，请稍后重试"}), 500

# 登出接口
@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    print("User logging out")  # 调试信息
    session.clear()
    # 对于AJAX请求返回JSON，对于直接访问返回重定向
    if request.method == 'POST':
        return jsonify({"msg": "成功退出登录"}), 200
    else:
        return redirect('/login')