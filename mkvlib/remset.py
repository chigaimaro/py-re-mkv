import configparser
import logging
from pathlib import Path
from mkvlib import remsys

log = logging.getLogger(__name__)


class AvSettings:
    def __init__(self):
        self.settings_file = "settings.ini"
        self.utils = {}
        self.folders = {}
        self.session_limits = {}
        self.file_processing = {
            "auto_temp": False
        }
        self.prefs = {}
        self.init_settings()

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
                    self.utils.update({each_key: each_value})
                elif 'Folders' in each_section:
                    each_value = Path(each_value)
                    self.folders.update({each_key: each_value})
                elif 'SessionLimits' in each_section:
                    self.session_limits.update({each_key: int(each_value)})
                elif 'FileProcessing' in each_section:
                    self.file_processing.update(
                        {each_key: bool(each_value)})
                elif 'Preferences' in each_section:
                    self.prefs.update(
                        {each_key: tuple(str(each_value).split(','))})
                log.debug(f"{each_key}: {each_value}")
        log.info("Loaded settings from file")

    def test_utils(self):
        log.info("Testing for dependencies")
        for key, value in self.utils.items():
            log.debug(f"Checking for: {value}")
            if not Path(value).exists():
                remsys.exit_on_error(f"Dependency: {key} not found, quitting")
            else:
                log.info(f"Found dependency: {key}")

    def test_folders(self):
        log.info("Testing Folder paths")
        for key, value in self.folders.items():
            results = Path(value).exists()
            if not results and key == 'input' or 'output':
                remsys.exit_on_error(
                    f"{key} directory not found, please verify path. quitting"
                )
            elif not results and key == 'temp':
                self.file_processing["auto_temp"] = True
                log.warning(
                    f"{key} directory not found, using automatic settings.")

    def init_settings(self):
        self.read_config_file()
        self.test_utils()
        self.test_folders()

    def clear_all(self):
        self.utils.clear()
        self.folders.clear()
        self.session_limits.clear()
        self.file_processing.clear()
        self.prefs.clear()
