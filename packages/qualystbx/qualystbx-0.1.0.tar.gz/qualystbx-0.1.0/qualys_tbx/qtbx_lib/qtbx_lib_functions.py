import sys
import os
import ctypes
from pathlib import Path
from datetime import datetime

required_modules_to_check = ['requests', 'lxml', 'xmltodict', 'psutil']


def get_utc_datetime():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def check_modules_installed(modules):
    missing_modules = []
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("Error: Missing required Python modules. Please install the following modules and try again:")
        for missing_module in missing_modules:
            print(f"- {missing_module}")
        sys.exit(1)


def is_admin_or_root():
    if os.name == 'nt':
        # Windows system
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    elif os.name == 'posix':
        # Linux/Unix system
        return os.geteuid() == 0  # True if user's effective UID is 0 (root)
    else:
        print(f"EnvironmentError: Unsupported operating system: {os.name}")

def check_is_admin_or_root():
    if is_admin_or_root():
        print(f"!!! Warning: The user running this application is root or administrator: {os.name}")
        print(f"!!! Advise running as non-root user.")
    else:
        pass


def get_logger(logger=print, log_level="info"):
    if logger == print:
        return print
    elif logger == "info":
        return logger.info
    elif logger == "warning":
        return logger.warning
    elif logger == "error":
        return logger.error
    else:
        return logger.debug

def remove_file_safely(file_path, message_hint=None, logger=print):
    path = Path(file_path)
    try:
        path.unlink(missing_ok=True)  # No exception if file doesn't exist
        logger = get_logger(logger, "info")
        logger(f"{message_hint} File removed: {file_path}")
    except PermissionError:
        logger = get_logger(logger, "error")
        logger(f"{message_hint} Permission denied: cannot delete the file {file_path}")
    except Exception as e:
        logger = get_logger(logger, "error")
        logger(f"{message_hint} An unexpected error occurred while trying to delete the file {file_path}: {e}")

def create_local_directory(dir_path, print_method=print):
    if os.path.exists(dir_path):
        if os.access(dir_path, os.W_OK):
            #print_method(f"Directory '{dir_path}' already exists and is writable. ")
            pass
        else:
            print_method(f"Directory '{dir_path}' exists but is not writable. Please address permissions issue and rerun.")
            sys.exit(1)
    else:
        try:
            os.makedirs(dir_path)
            # print_method(f"Directory '{dir_path}' created successfully.")
            pass
        except Exception as e:
            print_method(f"Error creating directory '{dir_path}'. Please address issue and rerun. Exception: {e}")
            sys.exit(1)


# Example usage
if __name__ == "__main__":
    check_modules_installed(required_modules_to_check)
    check_is_admin_or_root()
