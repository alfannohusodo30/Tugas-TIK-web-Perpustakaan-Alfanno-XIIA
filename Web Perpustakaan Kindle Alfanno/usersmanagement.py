import hashlib
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from config import (
    USERS_FILE,
    COLOR_BG,
    COLOR_CARD,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_INPUT,
    COLOR_DANGER,
    COLOR_DANGER_HOVER,
    HoverButton,
)


def load_json(filename, default):
    if not os.path.exists(filename):
        save_json(filename, default)
        return default.copy() if isinstance(default, list) else default.copy()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default.copy() if isinstance(default, list) else default.copy()


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users():
    return load_json(USERS_FILE, {})


def save_users(users):
    save_json(USERS_FILE, users)


def register_user(username, email, password):
    users = load_users()
    if username in users:
        return False, "Username sudah terdaftar."
    for user in users.values():
        if user["email"].lower() == email.lower():
            return False, "Email sudah terdaftar."
    users[username] = {"email": email, "password": hash_password(password)}
    save_users(users)
    return True, "Akun berhasil dibuat! Silakan Sign In."


def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username tidak ditemukan."
    if users[username]["password"] != hash_password(password):
        return False, "Password salah."
    return True, "Sign In berhasil."


def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return True
    return False


class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_user = None

        container = tk.Frame(self, bg=COLOR_BG, padx=30, pady=25)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="Manajemen Pengguna Perpustakaan",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(0, 15))

        table_card = tk.Frame(container, bg=COLOR_CARD, padx=20, pady=15)
        table_card.pack(fill="both", expand=True)

        columns = ("username", "email")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings")
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.column("username", width=200, stretch=True)
        self.tree.column("email", width=300, stretch=True)

        self.tree.pack(fill="both", expand=True, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self.select)

        btn_frame = tk.Frame(table_card, bg=COLOR_CARD)
        btn_frame.pack(fill="x")

        HoverButton(
            btn_frame,
            text="Hapus Pengguna",
            bg_normal=COLOR_DANGER,
            bg_hover=COLOR_DANGER_HOVER,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            command=self.delete,
        ).pack(side="left")

    def on_show(self):
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = load_users()
        for username, data in users.items():
            self.tree.insert("", "end", values=(username, data.get("email", "-")))

    def select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_user = values[0]

    def delete(self):
        if not self.selected_user:
            messagebox.showwarning("Peringatan", "Pilih pengguna dari tabel dahulu.")
            return

        if self.selected_user == self.controller.current_user:
            messagebox.showerror("Gagal", "Tidak bisa menghapus akun yang sedang aktif digunakan.")
            return

        if messagebox.askyesno("Konfirmasi", f"Hapus pengguna '{self.selected_user}'?"):
            if delete_user(self.selected_user):
                messagebox.showinfo("Berhasil", "Pengguna berhasil dihapus.")
                self.selected_user = None
                self.refresh()
            else:
                messagebox.showerror("Gagal", "Gagal menghapus pengguna.")