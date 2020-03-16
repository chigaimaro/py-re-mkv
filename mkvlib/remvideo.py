from mkvlib import remsys, remfiles
import json


class VideoProperties:
    def __init__(self, videofile):
        general = None
        video = None
        audio = None
        subtitles = None
        chapters = None
