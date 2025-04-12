from dataclasses import dataclass
from typing import Dict

@dataclass
class Colors:
    PRIMARY = "#000000"  # Changed to pure black for primary actions
    PRIMARY_DARK = "#1a1a1a"  # Slightly lighter black for hover
    SECONDARY = "#e4e4e7"  # Light gray for secondary actions
    SUCCESS = "#22c55e"  # Green
    DANGER = "#ef4444"  # Red
    WARNING = "#f59e0b"  # Amber
    BACKGROUND = "#ffffff"  # White
    TEXT = "#18181b"
    TEXT_SECONDARY = "#71717a"
    BORDER = "#e4e4e7"

@dataclass
class Styles:
    # Card styles
    CARD = {
        "background": Colors.BACKGROUND,
        "borderwidth": 1,
        "relief": "solid",
        "padding": 20,
    }

    # Button styles
    BUTTON_PRIMARY = {
        "background": Colors.PRIMARY,
        "foreground": Colors.BACKGROUND,
        "activebackground": Colors.PRIMARY_DARK,
        "activeforeground": Colors.BACKGROUND,
        "borderwidth": 0,
        "padding": (10, 8),  # Reduced padding
        "font": ("Helvetica", 10, "bold"),  # Slightly smaller font
        "width": 15,  # Narrower buttons
        "relief": "flat",
    }

    BUTTON_SECONDARY = {
        "background": Colors.BACKGROUND,
        "foreground": Colors.PRIMARY,
        "activebackground": Colors.SECONDARY,
        "activeforeground": Colors.PRIMARY,
        "borderwidth": 1,
        "padding": (10, 8),  # Reduced padding
        "font": ("Helvetica", 10),  # Slightly smaller font
        "width": 15,  # Narrower buttons
        "relief": "solid",
    }

    # Input styles
    INPUT = {
        "background": Colors.BACKGROUND,
        "foreground": Colors.TEXT,
        "borderwidth": 1,
        "relief": "solid",
        "padding": 12,
        "font": ("Helvetica", 11),
    }

    # Label styles
    LABEL = {
        "background": Colors.BACKGROUND,
        "foreground": Colors.TEXT,
        "font": ("Helvetica", 11, "bold"),
        "padding": (0, 5),
    }

    LABEL_HEADER = {
        "background": Colors.BACKGROUND,
        "foreground": Colors.TEXT,
        "font": ("Helvetica", 20, "bold"),
    }

    # Frame styles
    FRAME = {
        "background": Colors.BACKGROUND,
    }

def configure_styles(style):
    """Configure ttk styles with our custom theme"""
    style.configure("Card.TFrame", **Styles.CARD)
    style.configure("Primary.TButton", **Styles.BUTTON_PRIMARY)
    style.configure("Secondary.TButton", **Styles.BUTTON_SECONDARY)
    style.configure("Input.TEntry", **Styles.INPUT)
    style.configure("Label.TLabel", **Styles.LABEL)
    style.configure("Header.TLabel", **Styles.LABEL_HEADER)
    style.configure("Main.TFrame", **Styles.FRAME)

CATEGORIES = [
    "Food",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Shopping",
    "Healthcare",
    "Education",
    "Other"
] 