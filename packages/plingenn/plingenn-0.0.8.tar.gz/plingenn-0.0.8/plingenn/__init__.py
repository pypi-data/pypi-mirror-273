import os
from colorama import Fore
from datetime import datetime

class LogManager:
    def __init__(self, level):
        self.level = level
        self.color_map = {
            "info": (Fore.LIGHTWHITE_EX, "<*>"),
            "warning": (Fore.YELLOW, "<->"),
            "bad": (Fore.RED, "<!>"),
            "good": (Fore.GREEN, "<+>"),
            "dbg": (Fore.MAGENTA, "</>"),
        }

    def notime(self, *args, **kwargs):
        color, text = self.color_map.get(self.level, (Fore.LIGHTWHITE_EX, self.level))
        base = f"{color}{text.upper()}"
        for arg in args:
            base += f" {arg}"
        if kwargs:
            for key, value in kwargs.items():
                base += f" {key}={value}"
        print(base)

    def log(self, *args, **kwargs):
        color, text = self.color_map.get(self.level, (Fore.LIGHTWHITE_EX, self.level))
        time_now = datetime.now().strftime("%H:%M:%S")
        base = f"{Fore.CYAN}│{Fore.LIGHTBLACK_EX}{time_now}{Fore.CYAN}│ {color}{text.upper()}"
        
        for arg in args:
            base += f" {arg}"

        if kwargs:
            for key, value in kwargs.items():
                base += f" {key}={value}"
        print(base)

PROGRAM_NAME = "Plingenn"
VERSION = "1.0"

BASE_DIR = os.getenv('LOCALAPPDATA')

def getver():
    return VERSION

def getname():
    return PROGRAM_NAME

def rf(file_name):
    try:
        os.remove(file_name)
        print("File removed successfully:", file_name)
    except OSError as e:
        print(f"Error: {file_name} : {e.strerror}")

def rgb(relative_path, base_dir=BASE_DIR):
    rf(os.path.join(base_dir, relative_path))