import tkinter as tk
from tkinter import ttk
import requests
import subprocess
import os

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_data(raw_data):
    games = {}
    for line in raw_data.split('\n'):
        if '|' in line:
            name, info = line.split('|', 1)
            name = name.split('.')[0]
            games[name.strip()] = info.strip()
    return games

def on_select():
    global games
    selected_game = game_var.get()
    info = games[selected_game]
    #with open('selected_game_info.txt', 'w') as file:
    #    file.write(info)

    subprocess.run(['python3', 'ChessReplay.py', '--use_gui', '--agent1', 'MrReplay', '--agent2', 'MrReplay', '--time_control', '1', '--game_log_str', info])


def filter_games():
    filter_text = filter_var.get().lower()
    filtered_games = [name for name in games.keys() if filter_text in name.lower()]
    dropdown['values'] = filtered_games
    if filtered_games:
        dropdown.current(0)

def _fetch_games(url):
    def fetch_games():
        global games
        raw_data = fetch_data(url)
        games = dict()
        if raw_data:
            games = parse_data(raw_data)
        else:
            print('No games available.')
        if games:
            dropdown['values'] = list(games.keys())
            dropdown.current(0)

    return fetch_games


def main(url):
    global game_var, games, dropdown, filter_var
    raw_data = fetch_data(url)
    #with open('games.txt', 'r') as f:
    #    #raw_data = [l.replace('\n', '') for l in f.readlines()]
    #    raw_data = f.read()
    if raw_data:
        games = parse_data(raw_data)

        root = tk.Tk()
        root.title("Game Selector")
        root.minsize(200, 100)  # Set minimum window size

        filter_var = tk.StringVar()
        filter_entry = tk.Entry(root, textvariable=filter_var)
        filter_entry.grid(column=0, row=0, padx=10, pady=5)

        filter_button = tk.Button(root, text="Filter", command=filter_games)
        filter_button.grid(column=0, row=1, padx=7, pady=5)

        fetch_button = tk.Button(root, text="Fetch Games", command=_fetch_games(url))
        fetch_button.grid(column=1, row=2, padx=10, pady=5)

        game_var = tk.StringVar()
        # width is measured in characters
        dropdown = ttk.Combobox(root,
                                font=("Comic Sans", 10),
                                textvariable=game_var, width=30)

        dropdown['values'] = list(games.keys())
        #dropdown.grid(column=0, row=0)
        dropdown.grid(column=0, row=2, padx=10, pady=10)

        select_button = tk.Button(root, text="Select", command=on_select)
        #select_button.grid(column=0, row=1)
        select_button.grid(column=0, row=3, padx=10, pady=10)

        root.mainloop()
    else:
        print("Failed to fetch or parse data.")

if __name__ == "__main__":
    YOUR_WEBSERVER_URL = "https://seadronessee.cs.uni-tuebingen.de/dashboard_chess"  # Replace with your URL
    #YOUR_WEBSERVER_URL = "https://filesamples.com/samples/document/txt/sample3.txt"  # example:
    main(YOUR_WEBSERVER_URL)

