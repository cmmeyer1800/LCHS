from flask import (
    redirect,
    render_template,
    Blueprint,
    request,
    flash,
    url_for,
    send_from_directory,
    make_response
)
from lchs.models import Video
from werkzeug.utils import secure_filename
from flask_login import login_required
from lchs.content import getImgList, getVidList, CONTENT_FOLDER, getVideoLength
from lchs import db
from sqlalchemy import func
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


@main.route("/upload_photo", methods=["GET", "POST"])
@login_required
def upload_photo():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part uploaded")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(f"{CONTENT_FOLDER}/image", filename))
            return redirect(url_for("main.photo"))
    return render_template("upload_photo.html")


@main.route("/upload_video", methods=["GET", "POST"])
@login_required
def upload_video():
    if request.method == "POST":
        video = request.files["video"]
        if not video or video.filename == "":
            flash("No File Uploaded")
            return redirect(request.url)

        if request.form["title"] == "":
            flash("No Title Given")
            return redirect(request.url)
        title = request.form["title"]

        if request.form["genre"] == "None":
            genre = None
        else:
            genre = request.form["genre"]

        if request.form["actors"] == "":
            actors = None
        else:
            actors = request.form["actors"]

        if request.form["keywords"] == "":
            keywords = None
        else:
            keywords = request.form["keywords"]

        allVids = [u.id for u in Video.query.all()]
        if not allVids:
            id = 1
        else:
            id = max(allVids)+1

        thumb = request.files["thumb"]
        thumbPath = os.path.join(f"{CONTENT_FOLDER}/thumbnail", str(id))
        if thumb.filename != "":
            thumb.save(thumbPath)


        videoPath = os.path.join(f"{CONTENT_FOLDER}/video", str(id))
        video.save(videoPath)

        vidLength = getVideoLength(videoPath)

        newVid = Video(title=title, length=vidLength,
                        genre=genre, actors=actors, keywords=keywords)

        db.session.add(newVid)
        db.session.commit()
        return render_template("upload_video.html", success=True)

    else:
        return render_template("upload_video.html")

@main.route("/video", methods=["GET"])
@login_required
def videos():
    #vidList = getVidList()
    vids = Video.query.all()
    vidList = [(v.title, v.id) for v in vids]
    return render_template("videos.html", vidList=vidList)


@main.route("/video/<vid>", methods=["GET"])
@login_required
def video(vid):
    v = Video.query.filter_by(title=vid).first()
    if not v:
        return make_response("File not found", 400)

    return render_template("video.html", vid=v.id, title=v.title)


@main.route("/photo", methods=["GET"])
@login_required
def photo():
    photos = getImgList()
    return render_template("photo.html", photos=photos)
