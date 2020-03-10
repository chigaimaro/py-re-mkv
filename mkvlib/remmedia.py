# Contains media processing related functions
import logging
from mkvlib import remset

log = logging.getLogger(__name__)


class AvSession:
    def __init__(self):
        self.settings = remset.AvSettings()

