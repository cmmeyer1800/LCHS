from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tools import *

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TestingSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.view_functions['static'] = login_required(app.send_static_file)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)

@app.route('/login')
def login():
    return render_template('login.html', next=request.args.get('next'))

@app.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(f"/login?next={request.args.get('next')}")
    login_user(user, remember=remember)
    next = request.args.get('next')
    if next:
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('photo'))
    return render_template("upload.html")

@app.route('/video', methods=['GET', 'POST'])
@login_required
def video():
    vidList = getVidList()
    if request.method == 'GET':
        return render_template('video.html', vidList = vidList, vid = f"{vidList[0]}.mp4")

    if request.method == 'POST':
        for x in vidList:
            if x in request.form:
                vid = x
        return render_template('video.html', vidList = vidList, vid=f"{vid}.mp4")

@app.route('/photo', methods=['GET'])
@login_required
def photo():
    photos = getPhotoList()
    return render_template("photo.html", photos=photos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)