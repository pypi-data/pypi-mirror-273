import os
from colorama import Fore
from datetime import datetime
import ctypes

BASE_DIR = os.getenv('LOCALAPPDATA')

class LogManager:
    text_cache = {}

    def __init__(self, level, info_color=None):
        self.level = level
        self.info_color = info_color if info_color else Fore.CYAN
        self.color_map = {
            "info": (self.info_color, "<*>"),
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
        
    @staticmethod
    def st(text):
        system = os.name
        
        if system == 'nt':
            if text in LogManager.text_cache:
                cached_text = LogManager.text_cache[text]
            else:
                cached_text = text
                LogManager.text_cache[text] = cached_text

            ctypes.windll.kernel32.SetConsoleTitleW(f"{text} - {cached_text}")
        elif system == 'posix':
            print(f"\033]0;{text}\007")
        else:
            pass

    @staticmethod
    def cc():
        LogManager.text_cache.clear()

def rf(file_name):
    try:
        os.remove(file_name)
        print("File removed successfully:", file_name)
    except OSError as e:
        print(f"Error: {file_name} : {e.strerror}")

def rgb(relative_path, base_dir=BASE_DIR):
    rf(os.path.join(base_dir, relative_path))