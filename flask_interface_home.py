from flask import Flask, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import time
import threading
import json
from firebase import firebase as fb

app = Flask(__name__)

# 🔹 Connect to Firebase
fb_cnnctn = fb.FirebaseApplication("https://birds-2b89b-default-rtdb.europe-west1.firebasedatabase.app/", None)

# 🔹 Load and process CSV data
strk_data = pd.read_csv("Bird_strikes.csv", encoding="ISO-8859-1")
csv_breed_lst = strk_data["WildlifeSpecies"].tolist()
csv_strike_lst = strk_data["NumberStruckActual"].tolist()

# 🔹 Remove duplicates and unwanted entries
def sortbreed(df):
    return sorted(set(df) - {"Hawks, eagles, vultures", "Pigeons, doves"})
breed_lst = sortbreed(csv_breed_lst)

# 🔹 Function to get top N birds with most strikes
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

# 🔹 Pie chart function
def generate_pie_chart(labels, data, title):
    plt.pie(data, labels=labels)
    plt.title(title)
    plt.savefig("1.png")
    plt.close()

# 🔹 Track last processed value to avoid duplicates
last_n = None

# 🔹 Function to check Firebase for new data
def check_firebase():
    global last_n
    while True:
        fb_data = fb_cnnctn.get("/GraphingInfo/birds", None)
        if fb_data:
            latest_n = int(list(fb_data.values())[-1]['n'])  # Get latest 'n' value
            if latest_n != last_n:  # Only update if new value detected
                last_n = latest_n
                topnbreeds_lst, topnstrikes_lst = topnbirdsfunct(latest_n, breed_lst, csv_strike_lst)
                generate_pie_chart(topnbreeds_lst, topnstrikes_lst, f"Top {latest_n} Birds in Strikes")
                print(f"Updated graph for top {latest_n} birds.")
        time.sleep(5)  # Wait 5 seconds before checking again

# 🔹 Run Firebase checker in the background
threading.Thread(target=check_firebase, daemon=True).start()

# 🔹 Flask route to trigger manual updates
@app.route("/update", methods=["GET"])
def update():
    check_firebase()
    return jsonify({"status": "Checked Firebase"})

if __name__ == "__main__":
    app.run(debug=True)

