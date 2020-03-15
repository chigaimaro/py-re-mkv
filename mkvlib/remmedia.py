# Contains media processing related functions
import logging
from mkvlib import remset, remfiles

log = logging.getLogger(__name__)


class RemSession:
    def __init__(self):
        self.settings = remset.AvSettings()
        self.queue = sorted(self.initialize_queue())
        self.current_file_map = None

    def __next__(self):
        pass

    def initialize_queue(self):
        queue = []
        for ext in remfiles.mkv_extensions:
            new_ext = str('**/' + ext)
            queue.extend(self.settings.folders['input-folder'].glob(new_ext))
        return queue

    # TODO Create File map function
