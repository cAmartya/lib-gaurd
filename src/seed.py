from app import app, db

from models import User

def user_seed():
    # Add user - test
    with app.app_context():
        if User.query.filter_by(username="test").first() is None:
            user = User(name="test", username="test", id=None, password="")
            user.set_password("test")
            db.session.add(user)
            db.session.commit()