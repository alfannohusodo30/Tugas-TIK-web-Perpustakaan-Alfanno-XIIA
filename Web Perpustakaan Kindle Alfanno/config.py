import os
import tkinter as tk
from tkinter import ttk

APP_NAME = "Perpustakaan Kindle"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users.json")
BOOKS_FILE = os.path.join(BASE_DIR, "books.json")
BORROWINGS_FILE = os.path.join(BASE_DIR, "borrowings.json")

# Palet Warna Modern Kindle Reader
COLOR_BG = "#0F172A"       # Slate Gelap
COLOR_SIDEBAR = "#1E293B"  # Navy Night
COLOR_CARD = "#1E293B"     # Panel Kontainer
COLOR_CARD_ALT = "#334155" # Card Highlight
COLOR_INPUT = "#334155"    # Field Input

COLOR_TEXT = "#F8FAFC"     # Teks Utama
COLOR_MUTED = "#94A3B8"    # Teks Sekunder

COLOR_ACCENT = "#F59E0B"        # Warm Kindle Gold
COLOR_ACCENT_HOVER = "#D97706"  # Gold Hover

COLOR_SUCCESS = "#10B981"        # Hijau Emerald
COLOR_SUCCESS_HOVER = "#059669"

COLOR_DANGER = "#EF4444"         # Merah Bawaan
COLOR_DANGER_HOVER = "#DC2626"

DEFAULT_BOOKS = [
    {
        "id": 1,
        "judul": "Laskar Pelangi",
        "penulis": "Andrea Hirata",
        "tahun": "2005",
        "stok": 5,
    },
    {
        "id": 2,
        "judul": "Bumi",
        "penulis": "Tere Liye",
        "tahun": "2014",
        "stok": 4,
    },
    {
        "id": 3,
        "judul": "Atomic Habits",
        "penulis": "James Clear",
        "tahun": "2018",
        "stok": 3,
    },
    {
        "id": 4,
        "judul": "Harry Potter",
        "penulis": "J.K. Rowling",
        "tahun": "1997",
        "stok": 4,
    },
]


class HoverButton(tk.Button):
    def __init__(self, parent, bg_normal, bg_hover, **kwargs):
        super().__init__(
            parent,
            bg=bg_normal,
            activebackground=bg_hover,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            relief="flat",
            **kwargs,
        )
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.bind("<Enter>", lambda e: self.config(bg=self.bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_normal))


def setup_theme():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#1E293B",
        foreground="#F8FAFC",
        fieldbackground="#1E293B",
        rowheight=36,
        font=("Segoe UI", 10),
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background="#334155",
        foreground="#F59E0B",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_ACCENT)],
        foreground=[("selected", "#0F172A")],
    )