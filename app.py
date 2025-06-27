from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)
print("[INFO] Flask app initialisée")

def load_names(filename):
    print(f"[DEBUG] Lecture de {filename}...")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
            print(f"[DEBUG] → {len(names)} lignes chargées depuis {filename}")
            return names
    except Exception as e:
        print(f"[ERROR] Échec de lecture de {filename} : {e}")
        return []

@app.route('/generate_gmails')
def generate_gmails():
    print("[DEBUG] ➤ Appel route /generate_gmails")

    try:
        n = int(request.args.get('n', 10))
        print(f"[DEBUG] Paramètre 'n' = {n}")
    except Exception as e:
        print(f"[ERROR] Mauvais paramètre 'n' : {e}")
        return jsonify({"error": "Invalid 'n' parameter"}), 400

    firstnames = load_names("firstnames.txt")
    lastnames = load_names("lastnames.txt")

    if not firstnames or not lastnames:
        print("[ERROR] Les listes de noms sont vides ou introuvables.")
        return jsonify({"error": "Missing name files"}), 500

    gmails = []
    for _ in range(n):
        firstname = random.choice(firstnames)
        lastname = random.choice(lastnames)
        numbers = ''.join(random.choices(string.digits, k=random.randint(0, 2)))
        email = f"{firstname.lower()}.{lastname.lower()}{numbers}@gmail.com"
        gmails.append(email)

    print(f"[DEBUG] ✔ {len(gmails)} adresses générées avec succès.")
    return jsonify({"emails": gmails})

if __name__ == '__main__':
    print("[INFO] Lancement de l'application Flask sur 0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000)
