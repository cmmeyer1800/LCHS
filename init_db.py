from lchs import create_app, db
from lchs.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import func

app = create_app()

with app.app_context():
    db.create_all()

    admin = User(email="admin@lchs.com", password = generate_password_hash("password", method='sha256'), name="admin")

    db.session.add(admin)

    db.session.commit()