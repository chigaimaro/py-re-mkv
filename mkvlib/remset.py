import configparser
import logging
import os
from mkvlib import remsys
from pathlib import Path

log = logging.getLogger(__name__)


def read_config_file(input_file):
    """
    :param input_file:
    :return:
    """
    default_cfg = {
        'utils': {
            'ffmpeg': 'ffmpeg',
            "ffprobe": "ffprobe",
            "ccextract": "ccextractorwin",
            "mkvmerge": "mkvmerge",
            "mkvinfo": "mkvinfo",
            "mkvextract": "mkvextract",
            "mediainfo": "mediainfo"
        },
        'folders': {
            "input-folder": "[A\\File\\Path]",
            "output-folder": "[A\\File\\Path]",
            "temp-folder": "[A\\File\\Path]"
        },
        'session-limits': {
            "log-limit": "10",
            "file-history": "1000",
            "open-sessions": "1"
        },
        'file-processing': {
            "completion-tracking": "true",
            "subfolder-scan": "false",
            "audio-normalization": "false",
            "interlace-detection": "false",
            "delete-original-file": "false",
            "cc-extraction": "false"
        },
        'preferences': {
            "preferred-subtitles": "eng,jpn,deu,chi",
            "preferred-audio": "jpn,deu,chi,eng"
        }
    }

    settings = {
        'utils' : {},
        'folders' : {},
        'session_limits' : {},
        'file_processing' : {},
        'preferences' : {}
    }

    def test_ini_path(file_path):
        return os.path.isfile(file_path)

    def create_ini_file():
        new_ini = Path.cwd().joinpath('settings.ini')
        try:
            with open(new_ini, 'w') as configfile:
                remconfig.write(configfile)
        except IOError as ini_err:
            remsys.exit_on_error(ini_err)
        return new_ini

    def test_config_utils(file_path):
        test_results = {key: value if os.path.exists(value) else remsys.exit_on_error(f"{key} not found")
                        for key, value in file_path}
        return test_results

    def test_config_folders(input_folder):
        test_results = {}
        test_var = None
        for key, value in input_folder:
            test_results.update(test_folder_path(key, value))
        return test_results

    def test_folder_path(key, value):
        """
        :param key:
        :param value:
        :return:
        """
        test_results = os.path.isdir(value)
        if not test_results and (key == 'input-folder' or key == 'output-folder'):
            remsys.exit_on_error(
                f"{key} directory not found, please verify path. quitting"
            )
        elif test_results and (key == 'input-folder' or key == 'output-folder'):
            return {key: Path(value)}
        elif not test_results and key == 'temp-folder':
            return {"auto_temp": True}
        elif test_results and key == 'temp-folder':
            return {key: value}

    remconfig = configparser.ConfigParser(allow_no_value=True, strict=True)
    remconfig.read_dict(default_cfg)
    if not test_ini_path(input_file):
            input_file = create_ini_file()
            print('hi')

    try:
        remconfig.read(input_file)
        if 'utils' in remconfig.sections():
            results = test_config_utils(remconfig.items('utils'))
            settings['utils'].update(results)
            results = None
        if 'folders' in remconfig.sections():
            results = test_config_folders(remconfig.items('folders'))
            settings['folders'].update(results)
            results = None
        if 'session-limits' in remconfig.sections():
            results = {key: int(value) if value.isdigit() else remsys.exit_on_error(f"{key} not a whole number")
                       for (key, value) in remconfig.items('session-limits')}
            settings['session_limits'].update(results)
            results = None
        if 'file-processing' in remconfig.sections():
            results = {key: bool(value) for  (key, value) in remconfig.items('file-processing')}
            print('hi')
    except (TypeError, ValueError, KeyError) as err:
       remsys.exit_on_error(err)
    return settings

settings_path = 'C:\\Users\\chigaimaro\\Projects\\py-re-mkv\\settings.ini'
read_config_file(settings_path)
