from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    # 创建 demo 用户 mammotion / 666
    if not User.query.filter_by(username='mammotion').first():
        user = User(username='mammotion',role='admin')
        user.set_password('666')
        db.session.add(user)
        db.session.commit()
        print("创建 admin 用户 mammotion / 666")

    if not User.query.filter_by(username='mammotion_bak').first():
        user = User(username='mammotion_bak',role='annotator')
        user.set_password('666')
        db.session.add(user)
        db.session.commit()
        print("创建 annotator 用户 mammotion_bak / 666")
