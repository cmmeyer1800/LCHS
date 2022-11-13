import os
import sys
import numpy as np
import cv2

def getVideoLength(filepath: str) -> float:
    """
    Obtains the duration of the video at the given filepath
    
    @param: filepath = path to video file to get duration of
    @returns: duration = the duration of the video in milliseconds
    @side_effects: None
    """

    video = cv2.VideoCapture(filepath)
    duration = video.get(cv2.CAP_PROP_POS_MSEC)

    return duration


def getVideoThumbnail(filepath: str) -> np.ndarray:
    """
    This function takes a path to a video file and then get a frame 2 seconds
    into the video to use as a thumbnail

    @param: filepath = path to video file to get thumbnail from
    @returns: thumb_file_path = path to thumbnail image created
    @side_effects: Creates a new file in the thumbnail directory
    """

    cap = cv2.VideoCapture(filepath)
    _, frame = cap.read()
    return frame