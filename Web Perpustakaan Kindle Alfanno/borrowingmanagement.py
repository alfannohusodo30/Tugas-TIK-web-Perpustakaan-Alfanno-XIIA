import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
from config import (
    BORROWINGS_FILE,
    COLOR_BG,
    COLOR_CARD,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_ACCENT,
    COLOR_ACCENT_HOVER,
    COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER,
    HoverButton,
)
from usersmanagement import load_json, save_json


def load_borrowings():
    return load_json(BORROWINGS_FILE, [])


def save_borrowings(data):
    save_json(BORROWINGS_FILE, data)


def borrow_book(username, book_id):
    from bookmanagement import load_books, save_books

    books = load_books()
    borrowings = load_borrowings()

    target_book = next((b for b in books if b["id"] == book_id), None)
    if not target_book:
        return False, "Buku tidak ditemukan."
    if target_book["stok"] <= 0:
        return False, "Stok buku habis."

    for b in borrowings:
        if (
            b["username"] == username
            and b["book_id"] == book_id
            and b["status"] == "Dipinjam"
        ):
            return False, "Kamu sedang meminjam buku ini."

    target_book["stok"] -= 1
    save_books(books)

    next_id = max([b["id"] for b in borrowings], default=0) + 1
    today = date.today().strftime("%Y-%m-%d")
    borrowings.append({
        "id": next_id,
        "username": username,
        "book_id": book_id,
        "judul": target_book["judul"],
        "tanggal_pinjam": today,
        "tanggal_kembali": "-",
        "status": "Dipinjam",
    })
    save_borrowings(borrowings)
    return True, f"Berhasil meminjam '{target_book['judul']}'."


def return_book(borrow_id):
    from bookmanagement import load_books, save_books

    books = load_books()
    borrowings = load_borrowings()

    target_borrow = next((b for b in borrowings if b["id"] == borrow_id), None)
    if not target_borrow:
        return False, "Data transaksi tidak ditemukan."
    if target_borrow["status"] == "Dikembalikan":
        return False, "Buku sudah dikembalikan."

    for book in books:
        if book["id"] == target_borrow["book_id"]:
            book["stok"] += 1
            break
    save_books(books)

    today = date.today().strftime("%Y-%m-%d")
    target_borrow["status"] = "Dikembalikan"
    target_borrow["tanggal_kembali"] = today
    save_borrowings(borrowings)
    return True, "Buku berhasil dikembalikan."


class BorrowPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_borrow_id = None
        self.selected_book_id = None

        container = tk.Frame(self, bg=COLOR_BG, padx=30, pady=25)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="Sistem Peminjaman & Pengembalian Buku",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(0, 15))

        top_frame = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15)
        top_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            top_frame,
            text="Daftar Buku Tersedia Untuk Dipinjam:",
            bg=COLOR_CARD,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        cols_book = ("id", "judul", "penulis", "stok")
        self.tree_books = ttk.Treeview(top_frame, columns=cols_book, show="headings", height=5)
        self.tree_books.heading("id", text="ID")
        self.tree_books.heading("judul", text="Judul")
        self.tree_books.heading("penulis", text="Penulis")
        self.tree_books.heading("stok", text="Stok")

        self.tree_books.column("id", width=50)
        self.tree_books.column("judul", width=300)
        self.tree_books.column("penulis", width=200)
        self.tree_books.column("stok", width=80)

        self.tree_books.pack(fill="x", pady=(0, 10))
        self.tree_books.bind("<<TreeviewSelect>>", self.select_book)

        HoverButton(
            top_frame,
            text="Pinjam Buku Terpilih",
            bg_normal=COLOR_ACCENT,
            bg_hover=COLOR_ACCENT_HOVER,
            fg="#0F172A",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.handle_borrow,
        ).pack(anchor="w")

        bottom_frame = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15)
        bottom_frame.pack(fill="both", expand=True)

        tk.Label(
            bottom_frame,
            text="Riwayat Transaksi Peminjaman:",
            bg=COLOR_CARD,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        cols_borrow = ("id", "username", "judul", "tgl_pinjam", "tgl_kembali", "status")
        self.tree_borrow = ttk.Treeview(bottom_frame, columns=cols_borrow, show="headings")
        self.tree_borrow.heading("id", text="ID Transaksi")
        self.tree_borrow.heading("username", text="Peminjam")
        self.tree_borrow.heading("judul", text="Judul Buku")
        self.tree_borrow.heading("tgl_pinjam", text="Tgl Pinjam")
        self.tree_borrow.heading("tgl_kembali", text="Tgl Kembali")
        self.tree_borrow.heading("status", text="Status")

        self.tree_borrow.pack(fill="both", expand=True, pady=(0, 10))
        self.tree_borrow.bind("<<TreeviewSelect>>", self.select_borrow)

        HoverButton(
            bottom_frame,
            text="Kembalikan Buku Terpilih",
            bg_normal=COLOR_SUCCESS,
            bg_hover=COLOR_SUCCESS_HOVER,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.handle_return,
        ).pack(anchor="w")

    def on_show(self):
        self.refresh()

    def refresh(self):
        from bookmanagement import load_books

        for item in self.tree_books.get_children():
            self.tree_books.delete(item)
        for b in load_books():
            self.tree_books.insert("", "end", values=(b["id"], b["judul"], b["penulis"], b["stok"]))

        for item in self.tree_borrow.get_children():
            self.tree_borrow.delete(item)
        for br in load_borrowings():
            self.tree_borrow.insert(
                "",
                "end",
                values=(
                    br["id"],
                    br["username"],
                    br["judul"],
                    br["tanggal_pinjam"],
                    br["tanggal_kembali"],
                    br["status"],
                ),
            )

    def select_book(self, event):
        selected = self.tree_books.selection()
        if selected:
            self.selected_book_id = int(self.tree_books.item(selected[0], "values")[0])

    def select_borrow(self, event):
        selected = self.tree_borrow.selection()
        if selected:
            self.selected_borrow_id = int(self.tree_borrow.item(selected[0], "values")[0])

    def handle_borrow(self):
        if not self.selected_book_id:
            messagebox.showwarning("Peringatan", "Pilih buku dari tabel atas terlebih dahulu.")
            return

        ok, msg = borrow_book(self.controller.current_user, self.selected_book_id)
        if ok:
            messagebox.showinfo("Berhasil", msg)
            self.refresh()
        else:
            messagebox.showerror("Gagal", msg)

    def handle_return(self):
        if not self.selected_borrow_id:
            messagebox.showwarning("Peringatan", "Pilih transaksi dari tabel bawah terlebih dahulu.")
            return

        ok, msg = return_book(self.selected_borrow_id)
        if ok:
            messagebox.showinfo("Berhasil", msg)
            self.refresh()
        else:
            messagebox.showerror("Gagal", msg)