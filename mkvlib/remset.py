# Contains session settings
import configparser
import logging
import os
from pathlib import Path
from mkvlib import remfiles, remsys, remvideo

log = logging.getLogger(__name__)


def test_util(util_path):
    if not os.path.exists(util_path):
        remsys.exit_on_error(f"Dependency: {util_path} not found, quitting")
    else:
        log.info(f"Found dependency: {util_path}")
        return Path(util_path)


class RemSession:
    def __init__(self):
        self.settings_file = "settings.ini"
        self.utils = {}
        self.folders = {
            "auto_temp": True
        }
        self.session_limits = {}
        self.file_processing = {}
        self.preferences = {}
        self.read_config_file()
        self.queue = sorted(self.initialize_queue())

    def read_config_file(self):
        config = configparser.ConfigParser(allow_no_value=True)
        try:
            log.info(f"Attempting to read: {self.settings_file}")
            config.read(self.settings_file)
        except FileNotFoundError as err:
            remsys.exit_on_error(f"{err.errno}: {err.strerror}")
        for each_section in config.sections():
            for (each_key, each_value) in config.items(each_section):
                if 'Utils' in each_section:
                    log.debug(f"Testing for dependency: {each_value}")
                    self.utils.update({each_key: test_util(each_value)})
                elif 'Folders' in each_section:
                    log.debug(f"Testing Folder path: {each_value}")
                    each_value = self.test_folder(each_value, each_key)
                    self.folders.update({each_key: each_value})
                elif 'SessionLimits' in each_section:
                    self.session_limits.update({each_key: int(each_value)})
                elif 'FileProcessing' in each_section:
                    self.file_processing.update(
                        {each_key: bool(each_value)})
                elif 'Preferences' in each_section:
                    self.preferences.update(
                        {each_key: tuple(str(each_value).split(','))})
                log.debug(f"{each_key}: {each_value}")
        log.info("Loaded settings from file")

    def initialize_queue(self):
        queue = []
        for extension in remfiles.container_extensions:
            queue.extend(self.folders['input-folder'].glob(remfiles.set_extension(extension)))
        return queue

    def test_folder(self, input_folder, folder_type):
        results = os.path.exists(input_folder)
        if not results and (folder_type == 'input-folder' or folder_type == 'output-folder'):
            remsys.exit_on_error(
                f"{input_folder} directory not found, please verify path. quitting"
            )
        elif results and folder_type == 'auto':
            self.folders["auto_temp"] = False
            log.info(f"{input_folder} found, not using automatic settings.")
        elif not results and folder_type == 'auto':
            self.folders["auto_temp"] = False
            log.warning(f"{input_folder} not found, using automatic settings.")
            input_folder = None
            return input_folder
        return Path(input_folder)

    def clear_all(self):
        self.utils.clear()
        self.folders.clear()
        self.session_limits.clear()
        self.file_processing.clear()
        self.preferences.clear()

    # TODO Create File map function
