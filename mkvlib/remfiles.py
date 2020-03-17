from mkvlib import remsys, remmeta
import json


class VideoProcessor:
    """Process video file"""
    def __init__(self, session):
        self.session = session
        self.file_parts = None
        self.info_global = None
        self.info_video = None
        self.info_audio = None
        self.info_subtitles = None
        self.info_chapters = None

