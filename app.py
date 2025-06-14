from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

def load_names(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@app.route('/generate_gmails')
def generate_gmails():
    n = int(request.args.get('n', 10))
    firstnames = load_names("firstnames.txt")
    lastnames = load_names("lastnames.txt")
    gmails = []
    for _ in range(n):
        firstname = random.choice(firstnames)
        lastname = random.choice(lastnames)
        numbers = ''.join(random.choices(string.digits, k=random.randint(2, 3)))
        email = f"{firstname.lower()}{lastname.lower()}{numbers}@gmail.com"
        gmails.append(email)
    return jsonify({"emails": gmails})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8000))  # Railway fournit automatiquement ce port
    app.run(host='0.0.0.0', port=port)
