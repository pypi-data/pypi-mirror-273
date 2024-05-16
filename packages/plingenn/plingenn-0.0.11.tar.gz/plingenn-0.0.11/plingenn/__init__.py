import os
from colorama import Fore
from datetime import datetime
import ctypes
from time import sleep
from typing import List, Union

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
    def st(text, secondtext=None):
        system = os.name
        
        if system == 'nt':
            if text in LogManager.text_cache:
                cached_text = LogManager.text_cache[text]
            else:
                cached_text = secondtext
                LogManager.text_cache[text] = cached_text

            ctypes.windll.kernel32.SetConsoleTitleW(f"{text} - {cached_text}")
        elif system == 'posix':
            print(f"\033]0;{text}\007")
        else:
            pass

    @staticmethod
    def cc():
        LogManager.text_cache.clear()

class ChoiceMaker:
    def __init__(self, text: str = "", input_type: str = "str", options: list = None, invalid: callable = None):
        self.text = text.strip()
        self.input_type = input_type.lower() if input_type else "str"
        self.options = options
        self.invalid = invalid

    def Choices(self, *args):
        while True:
            user_input = input(f"{Fore.RED}<~> {self.text}: {Fore.LIGHTBLACK_EX}")

            if user_input == "BACK":
                LogManager("info").notime("Going back...")
                sleep(0.7)
                if self.invalid:
                    self.invalid()
                return

            if user_input == "":
                LogManager("bad").notime("Invalid choice, please try again!")
                sleep(0.7)
                if self.invalid:
                    self.invalid()
                return
            
            if self.input_type == "int":
                if user_input.isdigit():
                    user_input = int(user_input)
                    if self.options and user_input in self.options:
                        action = args[user_input - 1] if user_input <= len(args) else None
                        if action:
                            action()
                        else:
                            LogManager("bad").notime(f"No function for: '{user_input}', please contact support!")
                        break
                    elif not self.options:
                        return user_input
                else:
                    LogManager("bad").notime(f"Invalid literal: '{user_input}', please try again!")
            else:
                if self.options and user_input in self.options:
                    action = args[self.options.index(user_input)]
                    if action:
                        action()
                    else:
                        LogManager("bad").notime(f"No function for: '{user_input}', please contact support!")
                    break
                elif not self.options:
                    return user_input

            if self.invalid:
                self.invalid()
            else:
                LogManager("bad").notime("Invalid choice, please try again!")

def rf(file_name):
    try:
        os.remove(file_name)
        print("File removed successfully:", file_name)
    except OSError as e:
        print(f"Error: {file_name} : {e.strerror}")

def rfb(relative_path, base_dir=BASE_DIR):
    rf(os.path.join(base_dir, relative_path))