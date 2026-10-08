import tkinter as tk
from tkinter import messagebox
from config import COLOR_CARD, COLOR_TEXT, COLOR_MUTED, COLOR_INPUT, COLOR_ACCENT, COLOR_ACCENT_HOVER, HoverButton
from usersmanagement import login_user


class SignInFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_CARD)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="Selamat Datang Kembali",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")

        tk.Label(
            self,
            text="Username",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(15, 3))
        self.in_user = tk.Entry(
            self,
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 11),
        )
        self.in_user.pack(fill="x", ipady=7)

        tk.Label(
            self,
            text="Password",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(12, 3))
        self.in_pass = tk.Entry(
            self,
            show="*",
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 11),
        )
        self.in_pass.pack(fill="x", ipady=7, pady=(0, 20))

        HoverButton(
            self,
            text="MASUK",
            bg_normal=COLOR_ACCENT,
            bg_hover=COLOR_ACCENT_HOVER,
            fg="#0F172A",
            font=("Segoe UI", 10, "bold"),
            pady=10,
            command=self.handle_signin,
        ).pack(fill="x")

    def handle_signin(self):
        username = self.in_user.get().strip()
        password = self.in_pass.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi.")
            return

        success, msg = login_user(username, password)
        if success:
            messagebox.showinfo("Berhasil", msg)
            self.controller.open_main_window(username)
        else:
            messagebox.showerror("Gagal", msg)