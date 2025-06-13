from flask import Flask, jsonify, request
from names_dataset import NameDataset
import random
import string

app = Flask(__name__)

def generate_realistic_gmail(nd):
    first_name = random.choice(list(nd.first_names.keys()))
    last_name = random.choice(list(nd.last_names.keys()))
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
