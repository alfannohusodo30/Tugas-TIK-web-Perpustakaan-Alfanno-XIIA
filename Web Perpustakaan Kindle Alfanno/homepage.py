import tkinter as tk
from config import COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT, COLOR_SUCCESS
from bookmanagement import load_books
from borrowingmanagement import load_borrowings


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

    def on_show(self):
        for w in self.winfo_children():
            w.destroy()

        container = tk.Frame(self, bg=COLOR_BG, padx=35, pady=35)
        container.pack(fill="both", expand=True)

        hero = tk.Frame(container, bg=COLOR_CARD, padx=30, pady=25)
        hero.pack(fill="x", pady=(0, 25))

        tk.Label(
            hero,
            text=f"Selamat Datang, {self.controller.current_user}! 👋",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            hero,
            text="Ringkasan aktivitas inventaris dan sistem peminjaman buku digital.",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(5, 0))

        cards = tk.Frame(container, bg=COLOR_BG)
        cards.pack(fill="x", pady=(0, 25))

        books = load_books()
        borrowings = load_borrowings()

        total_titles = len(books)
        total_stok = sum(b["stok"] for b in books)
        total_borrowed = sum(1 for b in borrowings if b["status"] == "Dipinjam")

        self.create_card(
            cards, "📚 Total Judul", str(total_titles), COLOR_ACCENT
        ).pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.create_card(cards, "📦 Total Stok", str(total_stok), "#3B82F6").pack(
            side="left", fill="both", expand=True, padx=5
        )
        self.create_card(
            cards, "🔖 Buku Dipinjam", str(total_borrowed), COLOR_SUCCESS
        ).pack(side="left", fill="both", expand=True, padx=(10, 0))

        info = tk.Frame(container, bg=COLOR_CARD, padx=25, pady=20)
        info.pack(fill="both", expand=True)

        tk.Label(
            info,
            text="Panduan Akses Cepat",
            bg=COLOR_CARD,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))
        quick_text = (
            "• Koleksi Buku : Tambah, update, atau hapus buku Perpustakaan Kindle.\n"
            "• Peminjaman   : Kelola transaksi pinjam dan kembalikan buku.\n"
            "• Pengguna     : Kelola daftar pengguna perpustakaan.\n"
            "• Modus Layar  : Gunakan tombol F11 untuk beralih layar penuh."
        )
        tk.Label(
            info,
            text=quick_text,
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 10),
            justify="left",
            pady=5,
        ).pack(anchor="w")

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=COLOR_CARD, padx=20, pady=20)
        tk.Frame(card, bg=color, height=4).pack(fill="x", side="top", pady=(0, 10))
        tk.Label(
            card, text=title, bg=COLOR_CARD, fg=COLOR_MUTED, font=("Segoe UI", 11)
        ).pack(anchor="w")
        tk.Label(
            card,
            text=value,
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w", pady=(5, 0))
        return card