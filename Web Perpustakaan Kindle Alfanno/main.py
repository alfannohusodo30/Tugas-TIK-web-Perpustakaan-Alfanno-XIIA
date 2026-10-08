import tkinter as tk
from config import (
    APP_NAME,
    COLOR_BG,
    COLOR_CARD,
    COLOR_SIDEBAR,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_ACCENT,
    COLOR_INPUT,
    COLOR_DANGER,
    COLOR_DANGER_HOVER,
    HoverButton,
    setup_theme,
)
from signin import SignInFrame
from signup import SignUpFrame
from homepage import HomePage
from bookmanagement import BookPage
from borrowingmanagement import BorrowPage
from usersmanagement import UserPage


class AuthWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - Log In")
        self.geometry("480x600")
        self.resizable(True, True)
        self.minsize(420, 550)
        self.configure(bg=COLOR_BG)

        self.active_tab = "signin"
        self.build_ui()

    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()

        wrapper = tk.Frame(self, bg=COLOR_BG, padx=30, pady=30)
        wrapper.pack(fill="both", expand=True)

        header_frame = tk.Frame(wrapper, bg=COLOR_BG)
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame,
            text="📙 PERPUSTAKAAN KINDLE",
            bg=COLOR_BG,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 22, "bold"),
        ).pack()

        tk.Label(
            header_frame,
            text="Portal Akses Koleksi Digital",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=("Segoe UI", 10),
        ).pack(pady=(2, 0))

        card = tk.Frame(wrapper, bg=COLOR_CARD, padx=25, pady=25)
        card.pack(fill="both", expand=True)

        tab_frame = tk.Frame(card, bg=COLOR_CARD)
        tab_frame.pack(fill="x", pady=(0, 20))

        btn_in_bg = COLOR_ACCENT if self.active_tab == "signin" else COLOR_INPUT
        btn_up_bg = COLOR_ACCENT if self.active_tab == "signup" else COLOR_INPUT
        btn_in_fg = "#0F172A" if self.active_tab == "signin" else COLOR_TEXT
        btn_up_fg = "#0F172A" if self.active_tab == "signup" else COLOR_TEXT

        tk.Button(
            tab_frame,
            text="Sign In",
            bg=btn_in_bg,
            fg=btn_in_fg,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            pady=8,
            command=lambda: self.switch_tab("signin"),
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        tk.Button(
            tab_frame,
            text="Sign Up",
            bg=btn_up_bg,
            fg=btn_up_fg,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            pady=8,
            command=lambda: self.switch_tab("signup"),
        ).pack(side="right", fill="x", expand=True, padx=(4, 0))

        form_container = tk.Frame(card, bg=COLOR_CARD)
        form_container.pack(fill="both", expand=True)

        if self.active_tab == "signin":
            frame = SignInFrame(form_container, self)
        else:
            frame = SignUpFrame(form_container, self)
        frame.pack(fill="both", expand=True)

    def switch_tab(self, tab):
        self.active_tab = tab
        self.build_ui()

    def open_main_window(self, username):
        self.destroy()
        app = MainWindow(username)
        app.mainloop()


class MainWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.current_user = username
        self.title(APP_NAME)
        self.geometry("1200x740")
        self.resizable(True, True)
        self.minsize(950, 620)

        try:
            self.state("zoomed")
        except Exception:
            pass

        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        self.configure(bg=COLOR_BG)
        setup_theme()

        self.sidebar_frame = tk.Frame(self, bg=COLOR_SIDEBAR, width=250)
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack(side="left", fill="y")

        self.main_container = tk.Frame(self, bg=COLOR_BG)
        self.main_container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for Page in (HomePage, BookPage, BorrowPage, UserPage):
            frame = Page(self.main_container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.render_sidebar()
        self.show_page("HomePage")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    def render_sidebar(self):
        for w in self.sidebar_frame.winfo_children():
            w.destroy()

        brand = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR)
        brand.pack(fill="x", pady=25, padx=20)

        tk.Label(
            brand,
            text="📙 KINDLE",
            bg=COLOR_SIDEBAR,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")
        tk.Label(
            brand,
            text="Perpustakaan Digital Suite",
            bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 0))

        nav = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR)
        nav.pack(fill="x", pady=10)

        menu_items = [
            ("🏠  Beranda", "HomePage"),
            ("📚  Koleksi Buku", "BookPage"),
            ("🔄  Peminjaman", "BorrowPage"),
            ("👥  Pengguna", "UserPage"),
        ]

        for text, page in menu_items:
            HoverButton(
                nav,
                text=text,
                bg_normal=COLOR_SIDEBAR,
                bg_hover="#334155",
                fg=COLOR_TEXT,
                font=("Segoe UI", 11),
                anchor="w",
                padx=20,
                pady=12,
                command=lambda p=page: self.show_page(p),
            ).pack(fill="x", pady=2)

        HoverButton(
            nav,
            text="🖥️  Fullscreen (F11)",
            bg_normal=COLOR_SIDEBAR,
            bg_hover="#334155",
            fg=COLOR_MUTED,
            font=("Segoe UI", 10),
            anchor="w",
            padx=20,
            pady=8,
            command=self.toggle_fullscreen,
        ).pack(fill="x", pady=(20, 2))

        user_panel = tk.Frame(self.sidebar_frame, bg="#0F172A", padx=15, pady=15)
        user_panel.pack(side="bottom", fill="x", padx=15, pady=20)

        tk.Label(
            user_panel,
            text=f"👤 {self.current_user}",
            bg="#0F172A",
            fg=COLOR_ACCENT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        HoverButton(
            user_panel,
            text="Sign Out",
            bg_normal=COLOR_DANGER,
            bg_hover=COLOR_DANGER_HOVER,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            pady=6,
            command=self.logout,
        ).pack(fill="x")

    def show_page(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def logout(self):
        self.destroy()
        auth_app = AuthWindow()
        auth_app.mainloop()


if __name__ == "__main__":
    app = AuthWindow()
    app.mainloop()