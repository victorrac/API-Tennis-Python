from config import *

def show_player_search_window(root):
    search_window = tk.Toplevel(root)
    search_window.title("Search Player")

    # Labels and entry fields for first name and surname
    label_first_name = tk.Label(search_window, text="Enter player's first name:")
    label_first_name.pack()

    first_name_entry = tk.Entry(search_window)
    first_name_entry.pack()

    label_surname = tk.Label(search_window, text="Enter player's surname:")
    label_surname.pack()

    surname_entry = tk.Entry(search_window)
    surname_entry.pack()

    # Create a Text widget to display player info
    output_text = tk.Text(search_window, height=10, width=50)
    output_text.pack()

    def fetch_player_info():
        surname = surname_entry.get().strip()
        first_name = first_name_entry.get().strip()

        if surname and first_name:
            # Format the name as 'surname, first_name'
            formatted_name = f"{surname.title()}, {first_name.title()}"

            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # Extract player data
                rankings = data.get("rankings", [])
                players = {}

                # Collect player names and their details
                for ranking in rankings:
                    competitor_rankings = ranking.get("competitor_rankings", [])
                    for competitor in competitor_rankings:
                        player_name_data = competitor["competitor"].get("name")
                        player_info = {
                            "rank": competitor["rank"],
                            "points": competitor["points"],
                            "competitions_played": competitor["competitions_played"],
                            "country": competitor["competitor"].get("country"),
                            "country_code": competitor["competitor"].get("country_code")
                        }
                        if player_name_data:
                            players[player_name_data] = player_info

                # Search for the player and print the info in the Text widget
                if formatted_name in players:
                    output_text.delete(1.0, tk.END)  # Clear previous output
                    output_text.insert(tk.END, f"Details for {first_name} {surname}:\n")
                    output_text.insert(tk.END, f"Rank: {players[formatted_name]['rank']}\n")
                    output_text.insert(tk.END, f"Points: {players[formatted_name]['points']}\n")
                    output_text.insert(tk.END, f"Competitions Played: {players[formatted_name]['competitions_played']}\n")
                    output_text.insert(tk.END, f"Country: {players[formatted_name]['country']} ({players[formatted_name]['country_code']})\n")
                else:
                    output_text.delete(1.0, tk.END)  # Clear previous output
                    output_text.insert(tk.END, "Player not found.\n")
            else:
                output_text.delete(1.0, tk.END)  # Clear previous output
                output_text.insert(tk.END, f"Error: {response.status_code} - {response.text}\n")
        else:
            messagebox.showerror("Error", "Please enter both the player's first name and surname.")

    search_button = tk.Button(search_window, text="Search Player", command=fetch_player_info)
    search_button.pack()

