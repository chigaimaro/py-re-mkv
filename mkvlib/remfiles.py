container_extensions = ("WEBM", "MPG", "MP2", "MPEG", "MPE", "MPV", "MP4", "M4V", "AVI", "OGM", "WMV", "MOV", "QT",
                        "FLV", "SWF", "AVCHD", "MKV")


def set_extension(input_ext):
    return '**/*.{0}'.format(''.join('[%s%s]' % (e.lower(), e.upper()) for e in input_ext))
