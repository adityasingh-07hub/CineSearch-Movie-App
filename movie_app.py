import tkinter as tk
from tkinter import ttk

# ---------- Sample data (stands in for a backend/API) ----------
MOVIES = [
    {"title": "Inception", "year": 2010, "rating": 8.4, "language": "English", "genre": "Sci-Fi"},
    {"title": "The Dark Knight", "year": 2008, "rating": 9.0, "language": "English", "genre": "Action"},
    {"title": "Interstellar", "year": 2014, "rating": 8.7, "language": "English", "genre": "Sci-Fi"},
    {"title": "Avengers: Endgame", "year": 2019, "rating": 8.4, "language": "English", "genre": "Action"},
    {"title": "3 Idiots", "year": 2009, "rating": 8.4, "language": "Hindi", "genre": "Comedy"},
    {"title": "Dangal", "year": 2016, "rating": 8.3, "language": "Hindi", "genre": "Sports"},
    {"title": "Drishyam", "year": 2015, "rating": 8.2, "language": "Hindi", "genre": "Thriller"},
    {"title": "Vikram", "year": 2022, "rating": 8.3, "language": "Tamil", "genre": "Action"},
    {"title": "Kaithi", "year": 2019, "rating": 8.5, "language": "Tamil", "genre": "Thriller"},
    {"title": "Jai Bhim", "year": 2021, "rating": 8.7, "language": "Tamil", "genre": "Drama"},
    {"title": "Baahubali", "year": 2015, "rating": 8.0, "language": "Telugu", "genre": "Action"},
    {"title": "RRR", "year": 2022, "rating": 7.8, "language": "Telugu", "genre": "Action"},
    {"title": "Parasite", "year": 2019, "rating": 8.5, "language": "Korean", "genre": "Thriller"},
    {"title": "Train to Busan", "year": 2016, "rating": 7.6, "language": "Korean", "genre": "Horror"},
    {"title": "Your Name", "year": 2016, "rating": 8.4, "language": "Japanese", "genre": "Animation"},
    {"title": "Spirited Away", "year": 2001, "rating": 8.6, "language": "Japanese", "genre": "Animation"},
    {"title": "Amelie", "year": 2001, "rating": 8.3, "language": "French", "genre": "Romance"},
    {"title": "The Intouchables", "year": 2011, "rating": 8.5, "language": "French", "genre": "Comedy"},
]

# ---------- Colors ----------
BG = "#0f1117"
PANEL = "#171a23"
CARD = "#1a1d28"
RED = "#e50914"
TEXT = "#f1f1f1"
MUTED = "#aaaaaa"


class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CineSearch")
        self.root.geometry("1000x650")
        self.root.configure(bg=BG)

        self.watchlist = set()          # stores titles added to watchlist
        self.current_tab = "discover"
        self.columns = 3

        self.build_header()
        self.build_controls()
        self.build_movie_area()
        self.show_movies()

    # ---------- Header with tabs ----------
    def build_header(self):
        header = tk.Frame(self.root, bg=PANEL)
        header.pack(fill="x")

        tk.Label(header, text="🎬 CineSearch", font=("Segoe UI", 20, "bold"),
                 bg=PANEL, fg=RED).pack(side="left", padx=20, pady=12)

        self.watch_btn = tk.Button(header, text="My Watchlist (0)", font=("Segoe UI", 12),
                                   bg=PANEL, fg=MUTED, bd=0, cursor="hand2",
                                   command=lambda: self.switch_tab("watchlist"))
        self.watch_btn.pack(side="right", padx=15)

        self.discover_btn = tk.Button(header, text="Discover", font=("Segoe UI", 12, "bold"),
                                      bg=PANEL, fg=TEXT, bd=0, cursor="hand2",
                                      command=lambda: self.switch_tab("discover"))
        self.discover_btn.pack(side="right", padx=15)

    # ---------- Search, filters, sort ----------
    def build_controls(self):
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill="x", padx=20, pady=15)

        self.search_var = tk.StringVar()
        entry = tk.Entry(bar, textvariable=self.search_var, font=("Segoe UI", 12),
                         bg="#1f2330", fg=TEXT, insertbackground=TEXT, bd=0, width=28)
        entry.pack(side="left", ipady=6, padx=(0, 8))
        entry.bind("<Return>", lambda e: self.show_movies())

        tk.Button(bar, text="Search", font=("Segoe UI", 11), bg=RED, fg="white",
                  bd=0, padx=14, pady=4, cursor="hand2",
                  command=self.show_movies).pack(side="left", padx=(0, 15))

        self.lang_var = tk.StringVar(value="All Languages")
        langs = ["All Languages"] + sorted({m["language"] for m in MOVIES})
        self.make_dropdown(bar, self.lang_var, langs)

        self.rating_var = tk.StringVar(value="Any Rating")
        self.make_dropdown(bar, self.rating_var, ["Any Rating", "6+", "7+", "8+", "9+"])

        self.sort_var = tk.StringVar(value="Sort by")
        self.make_dropdown(bar, self.sort_var,
                           ["Sort by", "Rating (high to low)", "Year (newest first)", "Title (A-Z)"])

    def make_dropdown(self, parent, variable, values):
        box = ttk.Combobox(parent, textvariable=variable, values=values,
                           state="readonly", width=18, font=("Segoe UI", 10))
        box.pack(side="left", padx=5)
        box.bind("<<ComboboxSelected>>", lambda e: self.show_movies())

    # ---------- Scrollable area for cards ----------
    def build_movie_area(self):
        self.info_label = tk.Label(self.root, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10))
        self.info_label.pack(anchor="w", padx=22)

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.canvas, bg=BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>",
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    # ---------- Adjust layout when window size changes ----------
    def on_resize(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)   # card area fills full width
        new_columns = max(1, event.width // 320)                    # one column per ~320 px
        if new_columns != self.columns:
            self.columns = new_columns
            self.show_movies()

    # ---------- Tabs ----------
    def switch_tab(self, tab):
        self.current_tab = tab
        self.discover_btn.config(fg=TEXT if tab == "discover" else MUTED)
        self.watch_btn.config(fg=TEXT if tab == "watchlist" else MUTED)
        self.show_movies()

    # ---------- Filter + sort logic ----------
    def get_visible_movies(self):
        movies = MOVIES
        if self.current_tab == "watchlist":
            movies = [m for m in movies if m["title"] in self.watchlist]

        query = self.search_var.get().strip().lower()
        if query:
            movies = [m for m in movies if query in m["title"].lower()]

        if self.lang_var.get() != "All Languages":
            movies = [m for m in movies if m["language"] == self.lang_var.get()]

        if self.rating_var.get() != "Any Rating":
            min_rating = float(self.rating_var.get().replace("+", ""))
            movies = [m for m in movies if m["rating"] >= min_rating]

        sort = self.sort_var.get()
        if sort == "Rating (high to low)":
            movies = sorted(movies, key=lambda m: m["rating"], reverse=True)
        elif sort == "Year (newest first)":
            movies = sorted(movies, key=lambda m: m["year"], reverse=True)
        elif sort == "Title (A-Z)":
            movies = sorted(movies, key=lambda m: m["title"])
        return movies

    # ---------- Draw the cards ----------
    def show_movies(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.watch_btn.config(text=f"My Watchlist ({len(self.watchlist)})")
        movies = self.get_visible_movies()

        if not movies:
            text = ("No movies found." if self.current_tab == "discover"
                    else "Your watchlist is empty. Add movies from Discover!")
            self.info_label.config(text=text)
            return
        self.info_label.config(text=f"{len(movies)} movie(s)")

        for c in range(10):
            if c < self.columns:
                self.grid_frame.columnconfigure(c, weight=1, uniform="cards")
            else:
                self.grid_frame.columnconfigure(c, weight=0, uniform="", minsize=0)

        for i, movie in enumerate(movies):
            self.make_card(movie, i // self.columns, i % self.columns)

    def make_card(self, movie, row, col):
        card = tk.Frame(self.grid_frame, bg=CARD, width=10, height=170)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        card.pack_propagate(False)

        tk.Label(card, text=movie["title"], font=("Segoe UI", 14, "bold"),
                 bg=CARD, fg=TEXT, wraplength=260, anchor="w").pack(anchor="w", padx=12, pady=(12, 4))

        tk.Label(card, text=f"⭐ {movie['rating']}    {movie['year']}",
                 font=("Segoe UI", 11), bg=CARD, fg="#f5c518").pack(anchor="w", padx=12)

        tk.Label(card, text=f"{movie['language']}  •  {movie['genre']}",
                 font=("Segoe UI", 10), bg=CARD, fg=MUTED).pack(anchor="w", padx=12, pady=4)

        in_list = movie["title"] in self.watchlist
        tk.Button(card, text="Remove from Watchlist" if in_list else "+ Add to Watchlist",
                  font=("Segoe UI", 10), bg="#444" if in_list else RED, fg="white",
                  bd=0, cursor="hand2",
                  command=lambda t=movie["title"]: self.toggle_watchlist(t)
                  ).pack(side="bottom", fill="x", padx=12, pady=12)

    # ---------- Watchlist add/remove ----------
    def toggle_watchlist(self, title):
        if title in self.watchlist:
            self.watchlist.remove(title)
        else:
            self.watchlist.add(title)
        self.show_movies()


root = tk.Tk()
MovieApp(root)
root.mainloop()