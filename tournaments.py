from config import *
from weather import *

def show_atp_tournaments_window(root):
    tournaments_window = tk.Toplevel(root)
    tournaments_window.title("ATP Tournaments")

    label = tk.Label(tournaments_window, text="Enter the year to fetch ATP tournaments (e.g., 2022):")
    label.pack()

    year_entry = tk.Entry(tournaments_window)
    year_entry.pack()

    # Create a Text widget to display the output
    output_text = tk.Text(tournaments_window, height=15, width=50)
    output_text.pack()

    def fetch_atp_tournaments():
        year = year_entry.get().strip()
        try:
            year = int(year)
            url = f"https://ultimate-tennis1.p.rapidapi.com/tournament_list/atp/{year}/atpgs"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                tournaments = data.get("Tournaments", [])  # Correct key "Tournaments" (uppercase T)

                output_text.delete(1.0, tk.END)  # Clear previous output

                if tournaments:
                    output_text.insert(tk.END, f"ATP Tournaments for {year}:\n")
                    for idx, tournament in enumerate(tournaments, start=1):
                        name = tournament.get("Tournament Name")
                        location = tournament.get("Location")
                        date = tournament.get("Timestamp")
                        output_text.insert(tk.END, f"{idx}. {name} - Location: {location}, Date: {date}\n")
                else:
                    output_text.insert(tk.END, f"No ATP tournaments found for {year}.\n")
            else:
                output_text.insert(tk.END,
                                   f"Error fetching ATP tournaments: {response.status_code} - {response.text}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid year.")

    fetch_button = tk.Button(tournaments_window, text="Fetch Tournaments", command=fetch_atp_tournaments)
    fetch_button.pack()

def show_tournaments_by_city_window(root):
    city_window = tk.Toplevel(root)
    city_window.title("Tournaments by City")

    label = tk.Label(city_window, text="Enter the name of the city to search for tournaments:")
    label.pack()

    city_entry = tk.Entry(city_window)
    city_entry.pack()

    # Create a Text widget to display the tournament results
    output_text = tk.Text(city_window, height=15, width=50)
    output_text.pack()

    def fetch_tournaments_by_city():
        # Retrieve the city input from the user
        city = city_entry.get().strip()

        if city:
            city = city.strip().lower()  # Normalize input to lowercase and strip extra spaces
            years = [2020, 2021, 2022, 2023, 2024]  # Define the range of years to search for tournaments
            tournaments_found = False

            output_text.delete(1.0, tk.END)  # Clear previous output

            # Loop over the years to fetch the tournaments
            for year in years:
                url = f"https://ultimate-tennis1.p.rapidapi.com/tournament_list/atp/{year}/atpgs"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    tournaments = data.get("Tournaments", [])
                    for tournament in tournaments:
                        location = tournament.get("Location", "").lower()  # Normalize location to lowercase
                        if city in location:  # Check if city is a substring of the location
                            tournaments_found = True
                            name = tournament.get("Tournament Name", "Unknown Tournament")
                            date = tournament.get("Timestamp", "Unknown Date")
                            output_text.insert(tk.END, f"{name} - Location: {location.title()}, Date: {date}\n")
                else:
                    output_text.insert(tk.END, f"Error fetching tournaments for {year}: {response.status_code} - {response.text}\n")

            if not tournaments_found:
                output_text.insert(tk.END, f"No tournaments found in {city.title()} in the past 5 years.\n")

            # Create a new window to ask for weather or go back to the menu
            def open_weather_or_back_window():
                top_window = tk.Toplevel()  # Create a new top-level window
                top_window.title("Options")

                def on_weather_button_click():
                    fetch_weather_for_city(city, output_text)  # Pass output_text to display weather info
                    top_window.destroy()  # Close the options window after action

                def on_back_button_click():
                    top_window.destroy()  # Close the options window and go back to the menu

                weather_button = tk.Button(top_window, text="See Weather", command=on_weather_button_click)
                weather_button.pack(pady=5)

                back_button = tk.Button(top_window, text="Back to Menu", command=on_back_button_click)
                back_button.pack(pady=5)

            # Show the options window
            open_weather_or_back_window()
        else:
            messagebox.showerror("Error", "Please enter a city name.")

    fetch_button = tk.Button(city_window, text="Fetch Tournaments", command=fetch_tournaments_by_city)
    fetch_button.pack()