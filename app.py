from flask import Flask, jsonify
from names_dataset import NameDataset
import random
import string

app = Flask(__name__)

@app.route('/generate_gmail')
def generate_gmail():
    nd = NameDataset()
    first_name = random.choice(list(nd.first_names.keys()))
    last_name = random.choice(list(nd.last_names.keys()))
    numbers = ''.join(random.choices(string.digits, k=random.randint(2, 3)))
    email = f"{first_name.lower()}.{last_name.lower()}{numbers}@gmail.com"
    return jsonify({"email": email})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)