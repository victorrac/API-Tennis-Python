import tkinter as tk
from weather import *
from rankings import *
from config import *
from tournaments import *
from search import *

def main():
    global root
    root = tk.Tk()
    root.title("Tennis Project")

    button1 = tk.Button(root, text="View Rankings", command=lambda: show_rankings_window(root))
    button1.pack(pady=10)

    button2 = tk.Button(root, text="Search Player", command=lambda: show_player_search_window(root))
    button2.pack(pady=10)

    button3 = tk.Button(root, text="Top Players by Country", command=lambda: show_top_players_by_country_window(root))
    button3.pack(pady=10)

    button4 = tk.Button(root, text="ATP Tournaments", command=lambda: show_atp_tournaments_window(root))
    button4.pack(pady=10)

    button5 = tk.Button(root, text="Tournaments by City", command=lambda: show_tournaments_by_city_window(root))
    button5.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
