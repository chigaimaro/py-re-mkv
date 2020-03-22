import configparser
import logging
import os
from mkvlib import remsys

log = logging.getLogger(__name__)


def read_config_file(settings_file):
    """
    :param settings_file:
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
        'utils': {},
        'folders': {},
        'session_limits': {},
        'file_processing': {},
        'preferences': {}
    }

    def test_ini_path(file_path):
        log.debug(f'Testing {file_path}')
        tested_path = os.path.isfile(file_path)
        log.debug(f'Results from test: {tested_path}')
        return tested_path

    def create_ini_file():
        new_ini = os.path.join(os.getcwd(), 'settings.ini')
        log.warning(f"Creating settings file at:\n{new_ini}")
        try:
            with open(new_ini, 'w') as configfile:
                remconfig.write(configfile)
        except IOError as ini_err:
            remsys.exit_on_error(ini_err)
        log.info("Successfully created file")
        return new_ini

    remconfig = configparser.ConfigParser(allow_no_value=True, strict=True)
    remconfig.read_dict(default_cfg)

    if not test_ini_path(settings_file):
        log.warning("settings.ini missing, creating file")
        settings_file = create_ini_file()

    try:
        remconfig.read(settings_file)
        settings['utils'].update({key.replace('-', '_'): value for (key, value) in remconfig.items('utils')})
        settings['folders'].update({key.replace('-', '_'): value for (key, value) in remconfig.items('folders')})
        if not settings['folders']['temp_folder']:
            settings['folders'].update({"auto_temp": True})
        settings['session_limits'].update({key.replace('-', '_'): int(value)
                                           for (key, value) in remconfig.items('session-limits')})
        settings['file_processing'].update({key.replace('-', '_'): bool(value)
                                            for (key, value) in remconfig.items('file-processing')})
        settings['preferences'].update({key.replace('-', '_'): tuple(value.split(','))
                                        for (key, value) in remconfig.items('preferences')})
    except (TypeError, ValueError, KeyError) as err:
        remsys.exit_on_error(err)
    log.info("Successfully read settings.ini")
    return settings
