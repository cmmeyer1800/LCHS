from unicodedata import name
import sqlalchemy
from lchs import create_app, db
from lchs.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import func
from lchs.models import *
from lchs.settings import getSetting
from sqlalchemy import create_engine
import os

app = create_app()

[os.remove(os.path.join(f"{getSetting('contentFolder')}/photo", path)) for path in os.listdir(f"{getSetting('contentFolder')}/photo")]
[os.remove(os.path.join(f"{getSetting('contentFolder')}/thumbnail", path)) for path in os.listdir(f"{getSetting('contentFolder')}/thumbnail")]
[os.remove(os.path.join(f"{getSetting('contentFolder')}/video", path)) for path in os.listdir(f"{getSetting('contentFolder')}/video")]

with app.app_context():
    # engine = create_engine("postgresql://lchs_user:password@127.0.0.1/lchs")
    engine = create_engine("sqlite:///" + os.path.join(os.getcwd(), "db.lite"))
    
    User.__table__.drop(engine)
    Video.__table__.drop(engine)
    Photo.__table__.drop(engine)
    db.create_all()

    admin = User(email="admin@lchs.com", password = generate_password_hash("password", method='sha256'), name="admin", admin=True)
    non_admin = User(email="non_admin@lchs.com", password = generate_password_hash("password", method='sha256'), name="non_admin", admin=False)

    db.session.add(admin)
    db.session.add(non_admin)

    db.session.commit()