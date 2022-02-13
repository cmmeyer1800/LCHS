import os
import sys

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "heic", ".mp4"}

CONTENT_FOLDER = os.getenv("CONTENT_FOLDER")

if not CONTENT_FOLDER:
    sys.exit(
        "\u001b[31mCONTENT_FOLDER environmental variable must be set! Exiting...\u001b[0m"
    )


def checkVid(file: str) -> bool:
    return file.endswith(".mp4")


def checkImg(file: str) -> bool:
    return file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")


def getContentList(t: str = None) -> str:
    if t:
        if t == "video":
            return [x[0:-4] for x in os.listdir(CONTENT_FOLDER) if checkVid(x)]
        elif t == "img":
            return [x[0:-4] for x in os.listdir(CONTENT_FOLDER) if checkImg(x)]
        else:
            sys.exit(
                f'\u001b[31mType "{t}" passed to getContentList function is not valid\u001b[0m'
            )
    else:
        return os.listdir(CONTENT_FOLDER)
