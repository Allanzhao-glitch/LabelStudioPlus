from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask import render_template
from functools import wraps

db = SQLAlchemy()
migrate = Migrate()

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            # 检查用户是否登录
            if 'user_id' not in session:
                print(f"User not logged in, redirecting to login")  # 调试信息
                return redirect(url_for('auth.login_page'))
            
            # 检查用户角色
            user_role = session.get('user_role')
            print(f"User role: {user_role}, Required role: {role}")  # 调试信息
            if user_role != role:
                print(f"Role mismatch, redirecting to login")  # 调试信息
                return redirect(url_for('auth.login_page'))

            return fn(*args, **kwargs)
        return decorated
    return wrapper

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'),
                static_url_path='/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///demo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 设置session持久化
    app.config['SESSION_TYPE'] = 'filesystem'

        # 设置SESSION_COOKIE配置，支持跨域访问
    app.config['SESSION_COOKIE_DOMAIN'] = None  # 不限制域名
    app.config['SESSION_COOKIE_PATH'] = '/'     # cookie对整个应用有效
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # 如果使用HTTPS则设为True

    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 首页占位
    @app.route('/')
    def index():
        return redirect('/login')

    # 管理员面板
    @app.route('/admin')
    @role_required("admin")
    def admin_dashboard():
        print("Rendering admin dashboard")  # 调试信息
        return render_template("admin.html")

    # 标注员工作台
    @app.route('/annotator') 
    @role_required("annotator") 
    def annotator_dashboard():
        return render_template("annotator.html")

    return app