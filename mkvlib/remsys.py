import os
import logging
import errno
import sys
import hashlib
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from datetime import datetime

log = logging.getLogger(__name__)


# Setup logging
def config_logger(log_level="INFO"):
    """ Configures logger handler and logger stream to file
        :param log_level: Logging level, default level is INFO
        :return:
    """

    session_log_name = str(
        datetime.now().strftime("%Y%m%d-%H%M%S")) + '.log'
    log_path = Path.cwd().joinpath('logs')
    try:
        log_path.mkdir(parents=True, exist_ok=True)
    except IOError as err:
        message = f"{err.errno}: {err.strerror}"
        with open(session_log_name) as file:
            file.write(message)
        exit(1)
    log_format = logging.Formatter(
        '%(asctime)s : [%(module)s]: %(levelname)s : %(message)s')
    log_fh_handler = logging.FileHandler(
        filename=log_path.joinpath(session_log_name), mode='w')
    setup_log = logging.getLogger()
    setup_log.setLevel(log_level)
    log_fh_handler.setLevel(log_level)
    log_fh_handler.setFormatter(log_format)
    log.addHandler(log_fh_handler)
    return setup_log


# Check Python Version
def check_py_version():
    log.info("Checking version of Python")
    py_version = sys.version_info
    log.debug(py_version)
    if py_version[0] < 3 or py_version[1] < 7:
        exit_on_error("Please update your version of Python to at least 3.7.1")
    else:
        log.info("Python version check passes..")
        return True


# Clean up logs
def clear_logs(amount):
    # Takes an amount as a limit and removes log files over that limit
    log_file_list = sorted(Path.cwd().joinpath("logs").glob('*.log'))
    deletion_retry = 0
    while len(log_file_list) > amount and deletion_retry < 3:
        for file_to_delete in log_file_list:
            try:
                log.debug(
                    f"Attempting to remove: {file_to_delete}")
                os.remove(str(file_to_delete))
            except OSError:
                log.error(f"Error deleting {file_to_delete}")
                deletion_retry += 1
            else:
                log.info(f"Removed old log file: {file_to_delete}")


def test_path(input_path):
    if not os.path.exists(input_path):
        exit_on_error(f"{input_path} not found, quitting")
    else:
        log.info(f"Found: {input_path}")
        return Path(input_path)


# Run process
def invoke_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# Log error and exit
def exit_on_error(message):
    log.error(message)
    exit(1)
