# Contains media processing related functions
import logging
from mkvlib import remset

log = logging.getLogger(__name__)


class RemSession:
    def __init__(self):
        self.settings = remset.AvSettings()
        self.queue = None
        self.current_file_map = None
        # TODO - Add media related variables

    def __next__(self):
        pass

    def initialize_queue(self):
        self.settings = None
