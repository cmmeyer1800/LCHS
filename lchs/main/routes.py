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
import cv2
from lchs.models import Video, Photo
from flask_login import login_required, current_user
from lchs.content import getVideoLength, getVideoThumbnail
from lchs import db
import os
from lchs.settings import getSetting, getSettings, writeSettings
from sqlalchemy.exc import IntegrityError
import re


filepath_regex = re.compile(r"/^(?:[\w]\:|\/)(\/[a-z_\-\s0-9\.]+)+\.(json)$/i")

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/content/image/<filename>", methods=["GET"])
@login_required
def content_image(filename):
    return send_from_directory(f"{getSetting('contentFolder')}/photo", filename)


@main.route("/content/video/<filename>", methods=["GET"])
@login_required
def content_video(filename):    
    return send_from_directory(f"{getSetting('contentFolder')}/video", filename[:-4])


@main.route("/content/thumbnail/<filename>", methods=["GET"])
@login_required
def content_thumbnail(filename):
    return send_from_directory(f"{getSetting('contentFolder')}/thumbnail", filename)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/upload_photo", methods=["GET", "POST"])
@login_required
def upload_photo():
    if request.method == "POST":
        photo = request.files["photo"]
        if not photo or photo.filename == "":
            flash("No Photo Uploaded")
            return redirect(request.url)

        if request.form["title"] == "":
            flash("No Title Given")
            return redirect(request.url)
        title = request.form["title"]

        if request.form["people"] == "":
            people = None
        else:
            people = request.form["people"]

        if request.form["keywords"] == "":
            keywords = None
        else:
            keywords = request.form["keywords"]

        allPhotos = [u.id for u in Photo.query.all()]
        if not allPhotos:
            id = 1
        else:
            id = max(allPhotos)+1

        newVid = Photo(id=id, title=title, people=people, keywords=keywords)

        db.session.add(newVid)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Photo Title Already Exists!")
            return redirect(url_for("main.upload_photo"))

        photoPath = os.path.join(f"{getSetting('contentFolder')}/photo", str(id))
        photo.save(photoPath)

        return render_template("upload_photo.html", success=True)

    else:
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

        videoPath = os.path.join(f"{getSetting('contentFolder')}/video", str(id))
        video.save(videoPath)

        thumb = request.files["thumb"]
        thumbPath = os.path.join(f"{getSetting('contentFolder')}/thumbnail", str(id))
        if thumb.filename != "":
            thumb.save(thumbPath)
        else:
            _, buffer = cv2.imencode(".jpg", getVideoThumbnail(videoPath))
            buffer.tofile(thumbPath)


        vidLength = getVideoLength(videoPath)

        newVid = Video(id=id, title=title, length=vidLength,
                        genre=genre, actors=actors, keywords=keywords)

        db.session.add(newVid)
        
        try:
            db.session.commit()
        except IntegrityError:
            os.remove(videoPath)
            flash("Video Title Already Exists!")
            return redirect(url_for("main.upload_video"))

        return render_template("upload_video.html", success=True)

    else:
        return render_template("upload_video.html")


@main.route("/video/<vid>/delete", methods=["GET"])
@login_required
def videos_delete(vid):
    v = Video.query.filter_by(title=vid).first()
    if not v:
        return make_response("Video not found", 400)

    db.session.delete(v)
    db.session.commit()
    os.remove(os.path.join(f"{getSetting('contentFolder')}/video", str(v.id)))
    os.remove(os.path.join(f"{getSetting('contentFolder')}/thumbnail", str(v.id)))
    flash("Video Successfully Deleted")
    return render_template("videos.html", vidList = Video.query.all(), success=True)


@main.route("/video", methods=["GET", "POST"])
@login_required
def videos():
    if request.method == "GET":
        vids = Video.query.all()
        return render_template("videos.html", vidList=vids, search=False)
    else:
        search = request.form["search"]
        vids = Video.query.filter(Video.title.like(f"%{search}%")).all()
        return render_template("videos.html", vidList=vids, search=True)


@main.route("/video/<vid>", methods=["GET"])
@login_required
def video(vid):
    v = Video.query.filter_by(title=vid).first()
    if not v:
        return make_response("File not found", 400)

    return render_template("video.html", v=v)


@main.route("/photo", methods=["GET", "POST"])
@login_required
def photo():
    if request.method == "GET":
        p = Photo.query.all()
        return render_template("photo.html", photos=p, search=False)

    else:
        search = request.form["search"]
        p = Photo.query.filter(Photo.title.like(f"%{search}%")).all()
        return render_template("photo.html", photos=p, search=True)


@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if not current_user.admin and getSetting("onlyAdminChangeSettings").lower() == "true":
        return make_response("User must be admin to view/edit this page", 401)

    if request.method == "GET":
        settings = getSettings()
        return render_template("settings.html", settings=settings)

    else:
        sets = {}

        for k, v in request.form.items():
            if k == "onlyAdminChangeSettings":
                if v != "true" and v != "false":
                    return make_response(f"Bad input parameter: \"{v}\", for setting: \"onlyAdminChangeSettings\". Can only be \"true\" or \"false\"", 400)
                else:
                    sets[k] = v
            
            elif k == "contentFolder":
                if not os.path.isdir(v):
                    return make_response(f"Bad input parameter: \"{v}\", for setting: \"contentFolder\". Directory does not exist!", 400)
                else:
                    sets[k] = v
            else:
                make_response(f"Bad input parameter: {k}, setting does not exist", 400)
    
        writeSettings(sets)
        settings = getSettings()

        return render_template("settings.html", settings=settings)