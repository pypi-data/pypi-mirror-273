
import os
def __version__():
    return "0.1.1"

def obtain_wtao_path():
    return os.path.dirname(os.path.abspath(__file__))