from flask import Flask, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import threading
import time
from firebase import firebase as fb

# Flask App
app = Flask(__name__)

# Firebase Connection (using older module)
fb_cnnctn = fb.FirebaseApplication("https://birds-2b89b-default-rtdb.europe-west1.firebasedatabase.app/", None)

# Load Dataset
strk_data = pd.read_csv("Bird_strikes.csv", encoding="ISO-8859-1")
breed_lst = sorted(set(strk_data["WildlifeSpecies"].dropna().tolist()))

# Helper function to get top N birds
def topnbirdsfunct(n):
    sorted_data = strk_data.groupby("WildlifeSpecies")["NumberStruckActual"].sum().nlargest(n)
    return sorted_data.index.tolist(), sorted_data.values.tolist()

# Function to generate and save a pie chart
def generate_pie_chart(labels, data, title):
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.savefig("static/graph.png")
    plt.close()

# Function to process Firebase updates
def process_new_entry():
    fb_data = fb_cnnctn.get("/GraphingInfo/birds", None)
    if not fb_data:
        return

    latest_entry = list(fb_data.values())[-1]  # Get the latest value
    latest_n = int(latest_entry["n"])
    topnbreeds_lst, topnstrikes_lst = topnbirdsfunct(latest_n)
    generate_pie_chart(topnbreeds_lst, topnstrikes_lst, f'Top {latest_n} Birds in Strikes')

# Background Thread to Monitor Firebase
def check_firebase():
    last_checked = None
    while True:
        fb_data = fb_cnnctn.get("/GraphingInfo/birds", None)
        if fb_data and fb_data != last_checked:
            process_new_entry()
            last_checked = fb_data  # Store last processed data
        time.sleep(2)  # Check every 2 seconds

# Start background Firebase listener
threading.Thread(target=check_firebase, daemon=True).start()

@app.route("/check_updates", methods=["GET"])
def check_updates():
    process_new_entry()  # Manually trigger processing
    return jsonify({"status": "Graph updated"})

if __name__ == "__main__":
    app.run(debug=True)

