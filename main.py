from mkvlib import remsys, remset


def main():
    """ Main program loop """
    log = remsys.config_logger('DEBUG')
    log.info("Log file initialized")
    # Check version of python
    remsys.check_py_version()
    session = remset.RemSession()


if __name__ == '__main__':
    main()
else:
    exit(1)
