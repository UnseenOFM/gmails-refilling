from flask import Flask, jsonify, request
from names_dataset import NameDataset
import random
import string
import re
app = Flask(__name__)

def is_latin(s):
    return re.match(r'^[a-zA-Z]+$', s) is not None

def generate_realistic_gmail(nd):
    # Filtrer les prénoms et noms latins uniquement
    latin_first_names = [name for name in nd.first_names.keys() if is_latin(name)]
    latin_last_names = [name for name in nd.last_names.keys() if is_latin(name)]
    first_name = random.choice(latin_first_names)
    last_name = random.choice(latin_last_names)
    numbers = ''.join(random.choices(string.digits, k=random.randint(2, 3)))
    email = f"{first_name.lower()}.{last_name.lower()}{numbers}@gmail.com"
    return email

@app.route('/generate_gmails')
def generate_gmails():
    n = int(request.args.get('n', 10))  # nombre d'emails à générer, par défaut 10
    nd = NameDataset()
    gmails = [generate_realistic_gmail(nd) for _ in range(n)]
    return jsonify({"emails": gmails})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
