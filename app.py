from flask import Flask, jsonify, request
import random
import string
import os
import socket
import traceback

app = Flask(__name__)

@app.before_request
def log_request_info():
    print(f"\n[REQUEST] {request.method} {request.path}")
    print(f"[REQUEST HEADERS] {dict(request.headers)}")
    print(f"[REQUEST ARGS] {request.args}")

@app.after_request
def log_response_info(response):
    print(f"[RESPONSE] Status: {response.status_code}")
    return response

@app.route('/')
def health():
    return "✅ Flask is running", 200

def load_names(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
            print(f"[DEBUG] Loaded {len(names)} names from {filename}")
            return names
    except Exception as e:
        print(f"[ERROR] Failed to load {filename}: {e}")
        traceback.print_exc()
        return []

@app.route('/generate_gmails')
def generate_gmails():
    print("[DEBUG] ➤ /generate_gmails called")

    try:
        n = int(request.args.get('n', 10))
    except Exception as e:
        print(f"[ERROR] Invalid 'n' parameter: {e}")
        return jsonify({"error": "Invalid number parameter"}), 400

    print(f"[DEBUG] Requested {n} gmails")

    firstnames = load_names("firstnames.txt")
    lastnames = load_names("lastnames.txt")

    if not firstnames or not lastnames:
        print("[ERROR] One or both name lists are empty. Aborting generation.")
        return jsonify({"error": "Name lists are missing or empty"}), 500

    gmails = []
    for _ in range(n):
        firstname = random.choice(firstnames)
        lastname = random.choice(lastnames)
        numbers = ''.join(random.choices(string.digits, k=random.randint(2, 3)))
        email = f"{firstname.lower()}{lastname.lower()}{numbers}@gmail.com"
        gmails.append(email)

    print(f"[DEBUG] Successfully generated {len(gmails)} gmails")
    return jsonify({"emails": gmails})

@app.errorhandler(500)
def handle_500_error(error):
    print("[ERROR] Internal server error occurred")
    traceback.print_exc()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    hostname = socket.gethostname()
    print(f"[INFO] Starting Flask app")
    print(f"[ENV] PORT = {port}")
    print(f"[ENV] HOSTNAME = {hostname}")
    print(f"[INFO] Listening on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)
