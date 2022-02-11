import os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic'}

UPLOAD_FOLDER = '/home/collin/LCHS/static'

def getVidList() -> list:
    vids = [file[0:-4] for file in os.listdir("/home/collin/LCHS/static") if file.endswith(".mp4")]
    return vids

def getPhotoList() -> list:
    photos = [file for file in os.listdir("/home/collin/LCHS/static") if (
        file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".heic")
    )]
    return photos

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS