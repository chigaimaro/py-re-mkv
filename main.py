from mkvlib import remsys

def main():
    """ Main program loop """
    log = remsys.config_logger('DEBUG')
    log.info("Log file initialized")
    # Check version of python
    if not remsys.check_py_version():
        exit(0)


if __name__ == '__main__':
    main()
else:
    exit(1)