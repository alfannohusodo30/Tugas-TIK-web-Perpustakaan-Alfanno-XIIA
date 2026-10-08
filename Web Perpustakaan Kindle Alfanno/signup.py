import tkinter as tk
from tkinter import messagebox
from config import COLOR_CARD, COLOR_TEXT, COLOR_MUTED, COLOR_INPUT, COLOR_ACCENT, COLOR_ACCENT_HOVER, HoverButton
from usersmanagement import register_user


class SignUpFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_CARD)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="Buat Akun Perpustakaan Kindle",
            bg=COLOR_CARD,
            fg=COLOR_TEXT,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")

        tk.Label(
            self,
            text="Username",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(10, 2))
        self.up_user = tk.Entry(
            self,
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 10),
        )
        self.up_user.pack(fill="x", ipady=5)

        tk.Label(
            self,
            text="Email",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(8, 2))
        self.up_email = tk.Entry(
            self,
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 10),
        )
        self.up_email.pack(fill="x", ipady=5)

        tk.Label(
            self,
            text="Password",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(8, 2))
        self.up_pass = tk.Entry(
            self,
            show="*",
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 10),
        )
        self.up_pass.pack(fill="x", ipady=5)

        tk.Label(
            self,
            text="Konfirmasi Password",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(8, 2))
        self.up_confirm = tk.Entry(
            self,
            show="*",
            bg=COLOR_INPUT,
            fg="white",
            insertbackground="white",
            bd=0,
            font=("Segoe UI", 10),
        )
        self.up_confirm.pack(fill="x", ipady=5, pady=(0, 15))

        HoverButton(
            self,
            text="DAFTAR SEKARANG",
            bg_normal=COLOR_ACCENT,
            bg_hover=COLOR_ACCENT_HOVER,
            fg="#0F172A",
            font=("Segoe UI", 10, "bold"),
            pady=9,
            command=self.handle_signup,
        ).pack(fill="x")

    def handle_signup(self):
        username = self.up_user.get().strip()
        email = self.up_email.get().strip()
        password = self.up_pass.get()
        confirm = self.up_confirm.get()

        if not username or not email or not password:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Konfirmasi password tidak cocok.")
            return

        success, msg = register_user(username, email, password)
        if success:
            messagebox.showinfo("Berhasil", msg)
            self.controller.switch_tab("signin")
        else:
            messagebox.showerror("Gagal", msg)