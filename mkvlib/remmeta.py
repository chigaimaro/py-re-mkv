import json
import pathlib
from mkvlib import remsys

container_extensions = ("WEBM", "MPG", "MP2", "MPEG", "MPE", "MPV", "MP4", "M4V", "AVI", "OGM", "WMV", "MOV", "QT",
                        "FLV", "SWF", "AVCHD", "MKV")


def set_extension(input_ext):
    return '**/*.{0}'.format(''.join('[%s%s]' % (e.lower(), e.upper()) for e in input_ext))


def clean_duration(raw_time):
    try:
        clean_time = int(float(raw_time))
        return int(clean_time / 60)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


def clean_bitrate(raw_bit_rate):
    try:
        new_bitrate = int(int(raw_bit_rate) / 1000)
        return new_bitrate
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


def get_file_parts(video_name):
    parts = {
        'ext': pathlib.Path(video_name).suffix.split('.')[1],
        'fn': pathlib.Path(video_name).stem,
        'folder': pathlib.Path(video_name).parent,
        'fullname': pathlib.Path(video_name).name
    }
    return parts


def read_ffprobe(ffp_path, video_file):
    json_data = None
    ffp = [ffp_path, '-v', 'quiet', '-print_format', 'json',
           '-show_format', '-show_streams', '-show_programs', '-show_chapters',
           '-show_private_data', video_file]

    invoked_command = remsys.cmdRunCapture(ffp)

    if invoked_command.returncode == 0:
        json_data = json.loads(invoked_command.stdout)
        json_data['format']['bit_rate'] = clean_bitrate(json_data['format']['bit_rate'])
        json_data['format']['duration'] = clean_duration(json_data['format']['duration'])
    else:
        remsys.exit_on_error("Unable to load json data with FFprobe")
    return json_data
