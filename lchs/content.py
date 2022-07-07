import os
import sys
import cv2

# ALLOWED_IMAGES = getSetting("allowedImages")
# ALLOWED_VIDEOS = getSetting("allowedVideos")


# def checkVid(file: str) -> bool:
#     """
#     Returns whether or not the given file is a video of the type that we allow

#     True meaning it is, False meaning it is not
#     """

#     return True in [file.endswith(ext) for ext in ALLOWED_VIDEOS]


# def checkImg(file: str) -> bool:
#     """
#     Returns whether or not the given file is an image of the type that we allow

#     True meaning it is, False meaning it is not
#     """
    
#     # return (file.endswith(".jpg") or file.endswith(".jpeg")) and (
#     #     f"{file[0:-4]}.mp4" not in os.listdir(CONTENT_FOLDER)
#     # )
#     return True in [file.endswith(ext) for ext in ALLOWED_IMAGES]


# def getImgList() -> list[str]:
#     """
#     Creates a list of the images in the content folder and returns it
#     """
    
#     return [img for img in os.listdir(f"{CONTENT_FOLDER}/image") if checkImg(img)]


# def getVidList() -> list[str]:
#     """
#     Creates a list of the videos in the content folder and returns it
#     """
    
#     return [vid for vid in os.listdir(f"{CONTENT_FOLDER}/video") if checkVid(vid)]

def getVideoLength(filepath: str) -> float:

    video = cv2.VideoCapture(filepath)
    duration = video.get(cv2.CAP_PROP_POS_MSEC)

    return duration
