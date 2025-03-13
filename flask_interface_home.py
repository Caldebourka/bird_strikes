from flask import Flask, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import pygal
import time
import json
from firebase import firebase as fb

app = Flask(__name__)

# Firebase Connection
fb_cnnctn = fb.FirebaseApplication("https://birds-2b89b-default-rtdb.europe-west1.firebasedatabase.app/", None)

# Load and preprocess dataset
strk_data = pd.read_csv("Bird_strikes.csv", encoding="ISO-8859-1")
csv_breed_lst = strk_data["WildlifeSpecies"].tolist()
csv_strike_lst = strk_data["NumberStruckActual"].tolist()

# Sort breeds and remove duplicates
def sortbreed(df):
    return sorted(set(df) - {"Hawks, eagles, vultures", "Pigeons, doves"})
breed_lst = sortbreed(csv_breed_lst)

# Helper function to find top n birds
def topnbirdsfunct(n, b, s):
    temp_s = s.copy()
    l, bl = [], []
    x = 0
    while x < int(n):
        m = max(temp_s)
        ip = b[s.index(m)]
        if ip not in ["Unknown bird - small", "Unknown bird - medium", "Unknown bird - large"]:
            l.append(ip)
            bl.append(m)
            x += 1
        temp_s.remove(m)
    return l, bl

# Pie chart function
def generate_pie_chart(labels, data, title):
    plt.pie(data, labels=labels)
    plt.title(title)
    plt.tight_layout()
    plt.savefig("static/1.png")
    plt.close()

# Function to process new Firebase entries
def process_new_entry():
    fb_data = fb_cnnctn.get("/GraphingInfo/", None)
    if not fb_data:
        return

    bird_nval_lst = [int(value['n']) for key, value in fb_data.get('birds', {}).items()]
    if bird_nval_lst:
        latest_n = bird_nval_lst[-1]
        topnbreeds_lst, topnstrikes_lst = topnbirdsfunct(latest_n, breed_lst, csv_strike_lst)
        generate_pie_chart(topnbreeds_lst, topnstrikes_lst, f'Top {latest_n} Birds in Strikes')

@app.route("/check_updates", methods=["GET"])
def check_updates():
    process_new_entry()
    return jsonify({"status": "Graph updated"})

if __name__ == "__main__":
    app.run(debug=True)
