from flask import Flask, render_template, jsonify
import requests
import time
import os

app = Flask(__name__)

# Get your secret values from environment variables
API_TOKEN = os.environ.get("EXAROTON_API_KEY")
SERVER_ID = os.environ.get("EXAROTON_SERVER_ID")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start_server():
    try:
        start_url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/start/"
        r = requests.get(start_url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        # Optional: Poll until it's online (status 1)
        status_url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}"
        status = None
        for _ in range(15):  # check for ~30 seconds
            time.sleep(2)
            s = requests.get(status_url, headers=HEADERS).json()
            status = s["data"]["status"]
            if status == 1:
                break

        if status == 1:
            return jsonify({"success": True, "message": "Server is online!"})
        else:
            return jsonify({"success": True, "message": "Server is starting..."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/status")
def get_status():
    try:
        r = requests.get(f"https://api.exaroton.com/v1/servers/{SERVER_ID}", headers=HEADERS)
        r.raise_for_status()
        data = r.json()["data"]
        status = data["status"]
        name = data["name"]
        address = data["address"]
        return jsonify({"name": name, "status": status, "address": address})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
