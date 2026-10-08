import tkinter as tk
from tkinter import messagebox, ttk
from config import (
    BOOKS_FILE,
    DEFAULT_BOOKS,
    COLOR_BG,
    COLOR_CARD,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_INPUT,
    COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER,
    COLOR_DANGER,
    COLOR_DANGER_HOVER,
    HoverButton,
)
from usersmanagement import load_json, save_json
from borrowingmanagement import load_borrowings


def load_books():
    return load_json(BOOKS_FILE, DEFAULT_BOOKS)


def save_books(books):
    save_json(BOOKS_FILE, books)


def add_book(judul, penulis, tahun, stok):
    books = load_books()
    next_id = max([b["id"] for b in books], default=0) + 1
    books.append({
        "id": next_id,
        "judul": judul,
        "penulis": penulis,
        "tahun": tahun,
        "stok": stok,
    })
    save_books(books)


def update_book(book_id, judul, penulis, tahun, stok):
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            book["judul"] = judul
            book["penulis"] = penulis
            book["tahun"] = tahun
            book["stok"] = stok
            save_books(books)
            return True
    return False


def delete_book(book_id):
    books = load_books()
    borrowings = load_borrowings()
    for borrow in borrowings:
        if borrow["book_id"] == book_id and borrow["status"] == "Dipinjam":
            return False
    books = [b for b in books if b["id"] != book_id]
    save_books(books)
    return True


class BookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_id = None

        container = tk.Frame(self, bg=COLOR_BG, padx=30, pady=25)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="Koleksi & Inventaris Perpustakaan Kindle",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(0, 15))

        form_card = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15)
        form_card.pack(fill="x", pady=(0, 15))

        self.entries = {}
        inputs_frame = tk.Frame(form_card, bg=COLOR_CARD)
        inputs_frame.pack(fill="x", pady=(0, 10))

        fields = [
            ("Judul Buku", "judul", 22),
            ("Penulis", "penulis", 18),
            ("Tahun", "tahun", 8),
            ("Stok", "stok", 8),
        ]
        for label, name, w in fields:
            col = tk.Frame(inputs_frame, bg=COLOR_CARD)
            col.pack(side="left", padx=(0, 10), fill="x", expand=True)
            tk.Label(
                col,
                text=label,
                bg=COLOR_CARD,
                fg=COLOR_MUTED,
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            e = tk.Entry(
                col,
                bg=COLOR_INPUT,
                fg="white",
                insertbackground="white",
                bd=0,
                font=("Segoe UI", 10),
            )
            e.pack(fill="x", ipady=5, pady=(3, 0))
            self.entries[name] = e

        btn_frame = tk.Frame(form_card, bg=COLOR_CARD)
        btn_frame.pack(fill="x")

        HoverButton(
            btn_frame,
            text="Tambah Buku",
            bg_normal=COLOR_SUCCESS,
            bg_hover=COLOR_SUCCESS_HOVER,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.add,
        ).pack(side="left", padx=(0, 5))
        HoverButton(
            btn_frame,
            text="Update Buku",
            bg_normal="#3B82F6",
            bg_hover="#2563EB",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.update,
        ).pack(side="left", padx=5)
        HoverButton(
            btn_frame,
            text="Hapus Buku",
            bg_normal=COLOR_DANGER,
            bg_hover=COLOR_DANGER_HOVER,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.delete,
        ).pack(side="left", padx=5)
        HoverButton(
            btn_frame,
            text="Clear",
            bg_normal="#64748B",
            bg_hover="#475569",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.clear,
        ).pack(side="left", padx=5)

        table_card = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15)
        table_card.pack(fill="both", expand=True)

        search_frame = tk.Frame(table_card, bg=COLOR_CARD)
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            search_frame,
            text="🔍 Cari Buku:",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 8))
        self.search = tk.Entry(
            search_frame,
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 10),
            width=35,
        )
        self.search.pack(side="left", ipady=5)
        self.search.bind("<KeyRelease>", lambda e: self.refresh())

        columns = ("id", "judul", "penulis", "tahun", "stok")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings")

        widths = {"id": 60, "judul": 350, "penulis": 220, "tahun": 100, "stok": 90}
        headers = {
            "id": "ID",
            "judul": "Judul Buku",
            "penulis": "Penulis",
            "tahun": "Tahun",
            "stok": "Stok",
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], stretch=True)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = self.search.get().lower()
        for book in load_books():
            if (
                keyword
                and keyword not in book["judul"].lower()
                and keyword not in book["penulis"].lower()
            ):
                continue
            self.tree.insert(
                "",
                "end",
                values=(
                    book["id"],
                    book["judul"],
                    book["penulis"],
                    book["tahun"],
                    book["stok"],
                ),
            )

    def select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])

        self.entries["judul"].delete(0, tk.END)
        self.entries["judul"].insert(0, values[1])
        self.entries["penulis"].delete(0, tk.END)
        self.entries["penulis"].insert(0, values[2])
        self.entries["tahun"].delete(0, tk.END)
        self.entries["tahun"].insert(0, values[3])
        self.entries["stok"].delete(0, tk.END)
        self.entries["stok"].insert(0, values[4])

    def clear(self):
        self.selected_id = None
        for e in self.entries.values():
            e.delete(0, tk.END)

    def add(self):
        judul = self.entries["judul"].get().strip()
        penulis = self.entries["penulis"].get().strip()
        tahun = self.entries["tahun"].get().strip()
        stok = self.entries["stok"].get().strip()

        if not judul or not penulis or not tahun or not stok:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi.")
            return

        try:
            stok = int(stok)
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Stok harus angka positif.")
            return

        add_book(judul, penulis, tahun, stok)
        messagebox.showinfo("Berhasil", "Buku berhasil ditambahkan.")
        self.clear()
        self.refresh()

    def update(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih buku dari tabel dahulu.")
            return

        judul = self.entries["judul"].get().strip()
        penulis = self.entries["penulis"].get().strip()
        tahun = self.entries["tahun"].get().strip()

        try:
            stok = int(self.entries["stok"].get().strip())
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Stok harus angka positif.")
            return

        if update_book(self.selected_id, judul, penulis, tahun, stok):
            messagebox.showinfo("Berhasil", "Data buku diperbarui.")
            self.clear()
            self.refresh()
        else:
            messagebox.showerror("Gagal", "Buku tidak ditemukan.")

    def delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih buku dari tabel dahulu.")
            return

        if messagebox.askyesno("Konfirmasi", "Hapus buku ini dari daftar?"):
            if delete_book(self.selected_id):
                messagebox.showinfo("Berhasil", "Buku berhasil dihapus.")
                self.clear()
                self.refresh()
            else:
                messagebox.showerror("Gagal", "Buku sedang dipinjam oleh pengguna, tidak bisa dihapus.")