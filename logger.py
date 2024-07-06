from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init()


class Logger:
    """
    A simple logger class for printing colored messages to the console.
    """
    @staticmethod
    def info(message):
        print(Fore.BLUE + message + Style.RESET_ALL)

    @staticmethod
    def success(message):
        print(Fore.GREEN + message + Style.RESET_ALL)

    @staticmethod
    def error(message):
        print(Fore.RED + message + Style.RESET_ALL)
