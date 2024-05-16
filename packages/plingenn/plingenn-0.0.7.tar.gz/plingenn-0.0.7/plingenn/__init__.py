import os

PROGRAM_NAME = "Plingenn"
VERSION = "1.0"

BASE_DIR = os.getenv('LOCALAPPDATA')

def styled_print(message, style='normal'):
    styles = {
        'normal': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m',
    }
    if style in styles:
        print(styles[style] + message + styles['normal'])
    else:
        print(message)

def get_version():
    return VERSION

def get_program_name():
    return PROGRAM_NAME

def remove_file(base_dir=None, relative_path=None):
    if base_dir is None:
        base_dir = os.getcwd()
    file_path = os.path.join(base_dir, relative_path)
    try:
        os.remove(file_path)
        print("File removed successfully:", file_path)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

def remove_from_base(relative_path, base_dir=BASE_DIR):
    remove_file(base_dir, relative_path)