import os
import sys
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    WHITE = auto()
    BLACK = auto()

# Dictionnaire des codes ANSI pour les couleurs
COLOR_CODES = {
    Color.BLACK: "\033[30m",
    Color.RED: "\033[91m",
    Color.GREEN: "\033[92m",
    Color.YELLOW: "\033[93m",
    Color.BLUE: "\033[94m",
    Color.WHITE: "\033[97m",
    "reset": "\033[0m",
}

def supports_color():
    """Vérifie si le terminal supporte les couleurs."""
    if sys.platform.startswith('win'):
        return os.getenv('ANSICON') is not None or \
               'ANSICON' in os.environ or \
               'WT_SESSION' in os.environ or \
               'PYCHARM_HOSTED' in os.environ
    
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return True
    return False

def apply_color(text, color):
    """Applique la couleur spécifiée au texte, si supportée."""
    if supports_color():
        color_code = COLOR_CODES.get(color, COLOR_CODES["reset"])
        reset_code = COLOR_CODES["reset"]
        return f"{color_code}{text}{reset_code}"
    else:
        return text

def print_color(text: str, color: Color) -> None:
    """Affiche le texte avec la couleur spécifiée, si supportée."""
    print(apply_color(text, color))