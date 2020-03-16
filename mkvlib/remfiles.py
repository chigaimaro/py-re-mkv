import json
from mkvlib import remsys

container_extensions = ("WEBM", "MPG", "MP2", "MPEG", "MPE", "MPV", "MP4", "M4V", "AVI", "OGM", "WMV", "MOV", "QT",
                        "FLV", "SWF", "AVCHD", "MKV")


def set_extension(input_ext):
    return '**/*.{0}'.format(''.join('[%s%s]' % (e.lower(), e.upper()) for e in input_ext))


def cleanDuration(raw_time):
    clean_time = int(float(raw_time))
    newRate = 0
    if clean_time:
        newRate = int(clean_time / 60)
        return newRate
    else:
        return newRate


def cleanBitRate(raw_bit_rate):
    newRate = 0
    if not raw_bit_rate:
        return False
    elif raw_bit_rate.isdigit():
        return int(int(raw_bit_rate) / 1000)
    elif type(raw_bit_rate) is dict:
        return newRate
    else:
        return False