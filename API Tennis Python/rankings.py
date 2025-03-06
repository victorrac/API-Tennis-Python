from config import *

def show_rankings_window(root):
    rankings_window = tk.Toplevel(root)
    rankings_window.title("View Rankings")

    label = tk.Label(rankings_window, text="Enter 'men' or 'women' to see the rankings:")
    label.pack()

    gender_entry = tk.Entry(rankings_window)
    gender_entry.pack()

    label2 = tk.Label(rankings_window, text="How many top players do you want to see? (Enter an integer):")
    label2.pack()

    num_players_entry = tk.Entry(rankings_window)
    num_players_entry.pack()


    # Text widget to display the output
    global output_text
    output_text = tk.Text(rankings_window, height=20, width=60)
    output_text.pack()

    def fetch_rankings():
        gender = gender_entry.get().strip().lower()
        try:
            num_players = int(num_players_entry.get().strip())
            if num_players <= 0:
                messagebox.showerror("Error", "Please enter a positive integer.")
            else:
                if gender not in ["men", "women"]:
                    messagebox.showerror("Error", "Invalid gender. Please enter 'men' or 'women'.")
                    return

                if not isinstance(num_players, int) or num_players <= 0:
                    messagebox.showerror("Error", "Invalid number of players. Please enter a positive integer.")
                    return

                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    rankings = data.get("rankings", [])
                    players = []

                    for ranking in rankings:
                        if ranking.get("gender") == gender:
                            competitors = ranking.get("competitor_rankings", [])
                            players.extend(competitors)

                    # Clear the Text widget before displaying new data
                    output_text.delete(1.0, tk.END)

                    # Display the top players
                    total_players = len(players)
                    if total_players > 0:
                        output_text.insert(tk.END, f"Top {gender} players:\n")
                        for idx, player in enumerate(players[:num_players], start=1):  # Limit to user-specified number
                            name = player["competitor"]["name"]
                            rank = player["rank"]
                            points = player["points"]
                            output_text.insert(tk.END, f"{idx}. {name} - Rank: {rank}, Points: {points}\n")
                        if total_players < num_players:
                            output_text.insert(tk.END,
                                               f"There are only {total_players} {gender} players in the top rankings.\n")
                    else:
                        output_text.insert(tk.END, f"There are no {gender} players in the top rankings.\n")
                else:
                    output_text.insert(tk.END, f"Error fetching data: {response.status_code} - {response.text}\n")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    fetch_button = tk.Button(rankings_window, text="Fetch Rankings", command=fetch_rankings)
    fetch_button.pack()

def show_top_players_by_country_window(root):
    country_window = tk.Toplevel(root)
    country_window.title("Top Players by Country")

    # Labels and entry fields for country and number of players
    label = tk.Label(country_window, text="Enter the country to search for top players:")
    label.pack()

    country_entry = tk.Entry(country_window)
    country_entry.pack()

    label2 = tk.Label(country_window, text="How many top players do you want to see? (Enter an integer):")
    label2.pack()

    num_players_entry = tk.Entry(country_window)
    num_players_entry.pack()

    # Create a Text widget to display the output
    output_text = tk.Text(country_window, height=15, width=70)
    output_text.pack()

    def fetch_players_by_country():
        country = country_entry.get().strip()
        try:
            num_players = int(num_players_entry.get().strip())
            if num_players <= 0:
                messagebox.showerror("Error", "Please enter a positive integer.")
            else:
                country = country.lower()  # Convert input to lowercase for consistent matching
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    rankings = data.get("rankings", [])

                    male_players = []
                    female_players = []

                    for ranking in rankings:
                        gender = ranking.get("gender")
                        competitor_rankings = ranking.get("competitor_rankings", [])

                        for competitor in competitor_rankings:
                            player_country = competitor["competitor"].get("country", "").lower()

                            if player_country == country:
                                if gender == "men":
                                    male_players.append(competitor)
                                elif gender == "women":
                                    female_players.append(competitor)

                    # Display top male players or a message if none are found
                    output_text.delete(1.0, tk.END)  # Clear previous output

                    total_male_players = len(male_players)
                    if total_male_players > 0:
                        output_text.insert(tk.END, f"Top male players from {country.title()}:\n")
                        for idx, player in enumerate(male_players[:num_players], start=1):
                            name = player["competitor"]["name"]
                            rank = player["rank"]
                            points = player["points"]
                            output_text.insert(tk.END, f"{idx}. {name} - Rank: {rank}, Points: {points}\n")
                        if total_male_players < num_players:
                            output_text.insert(tk.END, f"There are only {total_male_players} male players in the top rankings from {country.title()}.\n")
                    else:
                        output_text.insert(tk.END, f"There are no male players from {country.title()} in the top rankings.\n")

                    # Display top female players or a message if none are found
                    total_female_players = len(female_players)
                    if total_female_players > 0:
                        output_text.insert(tk.END, f"\nTop female players from {country.title()}:\n")
                        for idx, player in enumerate(female_players[:num_players], start=1):
                            name = player["competitor"]["name"]
                            rank = player["rank"]
                            points = player["points"]
                            output_text.insert(tk.END, f"{idx}. {name} - Rank: {rank}, Points: {points}\n")
                        if total_female_players < num_players:
                            output_text.insert(tk.END, f"There are only {total_female_players} female players in the top rankings from {country.title()}.\n")
                    else:
                        output_text.insert(tk.END, f"There are no female players from {country.title()} in the top rankings.\n")
                else:
                    output_text.insert(tk.END, f"Error fetching data: {response.status_code} - {response.text}\n")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    fetch_button = tk.Button(country_window, text="Fetch Top Players", command=fetch_players_by_country)
    fetch_button.pack()
