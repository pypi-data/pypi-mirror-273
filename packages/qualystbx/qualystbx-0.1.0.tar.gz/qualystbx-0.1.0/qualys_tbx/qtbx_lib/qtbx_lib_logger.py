import logging
import getpass
import os
import sys
import json
from datetime import datetime
import time
from pathlib import Path
import qualys_tbx
global logger
global logger_info
global logger_warning
global logger_error

def set_logger(select_logger=None):
    global logger_info
    global logger_warning
    global logger_error
    if select_logger is None:
        logger_info = print
        logger_warning = print
        logger_error = print
    else:
        logger_info = select_logger.info
        logger_warning = select_logger.warning
        logger_error = select_logger.error

def setup_logging_stdout(log_level=logging.INFO, my_logger_prog_name=None):
    global logger
    global logging_is_on_flag
    global logger_datetime
    global logger_workflow_datetime
    global logger_iso_format_datetime
    global logger_database_format_datetime
    global my_logger_program_name_for_database_routine

    logging_is_on_flag = True
    logging.Formatter.converter = time.gmtime
    d = datetime.utcnow()
    td = f"{d.year}{d.month:02d}{d.day:02d}{d.hour:02d}{d.minute:02d}{d.second:02d}"
    logger_datetime = td
    logger_iso_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d}T{d.hour:02d}:{d.minute:02d}:{d.second:02d}Z"
    logger_database_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d} {d.hour:02d}:{d.minute:02d}:{d.second:02d}"
    my_logger_program_name_for_database_routine = my_logger_prog_name
    username = getpass.getuser()
    prog = Path(__file__).name
    if my_logger_prog_name is not None:
        prog = my_logger_prog_name

    prog = f"{prog}: {logger_datetime}"
    logger_workflow_datetime = prog

    logging.basicConfig(format=f"%(asctime)s | %(levelname)-8s | {prog:54s} | {username:15} | %(funcName)-60s | %(message)s",
                        level=log_level,)

    logger = logging.getLogger()  # Useful in qetl_manage_user when we want to set the name.
    logger.info(f"PROGRAM:     {sys.argv}")
    logger.info(f"{prog} VERSION: {qualys_tbx.__version__}")
    logger.info(f"LOGGING SUCCESSFULLY SETUP FOR STREAMING")
    set_logger(select_logger=logger)


class LoggerSetup:
    def __init__(self, log_level=logging.INFO, my_logger_prog_name=None):
        self.log_level = log_level
        self.my_logger_prog_name = my_logger_prog_name
        self.logger = None
        self.logging_is_on_flag = True
        self.configure_logging()

    def configure_logging(self):
        logging.Formatter.converter = time.gmtime
        d = datetime.utcnow()
        td = f"{d.year}{d.month:02d}{d.day:02d}{d.hour:02d}{d.minute:02d}{d.second:02d}"
        self.logger_datetime = td
        self.logger_iso_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d}T{d.hour:02d}:{d.minute:02d}:{d.second:02d}Z"
        self.logger_database_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d} {d.hour:02d}:{d.minute:02d}:{d.second:02d}"
        self.my_logger_program_name_for_database_routine = self.my_logger_prog_name
        username = getpass.getuser()
        prog = Path(__file__).name
        if self.my_logger_prog_name is not None:
            prog = self.my_logger_prog_name

        prog = f"{prog}: {self.logger_datetime}"
        self.logger_workflow_datetime = prog

        logging.basicConfig(format=f"%(asctime)s | %(levelname)-8s | {prog:54s} | {username:15} | %(funcName)-60s | %(message)s",
                            level=self.log_level)

        self.logger = logging.getLogger()  # Useful when we want to set the name in a specific context
        self.logger.info(f"PROGRAM:     {sys.argv}")
        self.logger.info(f"{prog} VERSION: {qualys_tbx.__version__}")
        self.logger.info("LOGGING SUCCESSFULLY SETUP FOR STREAMING")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "name": record.name,
            "level": record.levelname,
            "function": record.funcName,  # Include the function name
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


class QtbxLogger:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        if log_file_path.lower() != "stdout":
            self.validate_log_path()
        self.logger = self.setup_logger()

    def validate_log_path(self):
        if self.log_file_path.lower() == "stdout":
            return  # Skip validation for stdout
        # Ensure the directory exists or can be created
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        # Check if the file can be written to
        try:
            with open(self.log_file_path, 'a') as test_write:
                pass
        except IOError as e:
            print(f"Exception: {e}")
            print(f"Error: The log file '{self.log_file_path}' cannot be written to. Please check permissions or the path.")
            sys.exit(1)

    def setup_logger(self):
        # Create a logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create JSON formatter
        formatter = JsonFormatter()

        if self.log_file_path.lower() == "stdout":
            # Logging to stdout
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        else:
            # Logging to a file and stdout
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def main(my_logger_prog_name="main"):
    logger_setup = LoggerSetup(my_logger_prog_name="MyLoggerProgramName")
    logger_setup.logger.info("This is a test log message.")

if __name__ == "__main__":
    # For logging to a file
    # logger = QtbxLogger('/path/to/your/logfile.log')

    # For logging to stdout
#    logger = QtbxLogger("stdout")
#    logger.info("This is an info message")
#    logger.error("This is an error message")
     main(my_logger_prog_name="TEST")
