from flask import (
    redirect,
    render_template,
    Blueprint,
    request,
    flash,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from flask_login import login_required
from lchs.content import getImgList, getVidList, CONTENT_FOLDER
import os


main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/content/image/<filename>", methods=["GET"])
@login_required
def content_image(filename):
    return send_from_directory(f"{CONTENT_FOLDER}/image", filename)


@main.route("/content/video/<filename>", methods=["GET"])
@login_required
def content_video(filename):
    return send_from_directory(f"{CONTENT_FOLDER}/video", filename)


@main.route("/content/thumbnail/<filename>", methods=["GET"])
@login_required
def content_thumbnail(filename):
    return send_from_directory(f"{CONTENT_FOLDER}/thumbnail", filename)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(main.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("main.photo"))
    return render_template("upload.html")


@main.route("/video", methods=["GET"])
@login_required
def videos():
    vidList = getVidList()
    return render_template("videos.html", vidList=vidList)


@main.route("/video/<vid>", methods=["GET"])
@login_required
def video(vid):
    return render_template("video.html", vid=vid)


@main.route("/photo", methods=["GET"])
@login_required
def photo():
    photos = getImgList()
    return render_template("photo.html", photos=photos)
