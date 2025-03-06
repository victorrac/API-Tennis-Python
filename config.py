import requests
import tkinter as tk
from tkinter import messagebox

api_key = "TssBJzBWB3ilgRmQxFnf0GfVlVvD81B1fdPl7X9N"
locale = "en"
url = f"https://api.sportradar.com/tennis/production/v3/{locale}/rankings.json?api_key={api_key}"

ultimate_tennis_url = "https://ultimate-tennis1.p.rapidapi.com/tournament_list/atp/2022/atpgs"
headers = {
    "x-rapidapi-key": "5498a4d15emsh97d9e88061ece0cp1be2d1jsn444b19403a98",
    "x-rapidapi-host": "ultimate-tennis1.p.rapidapi.com"
}
