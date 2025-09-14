
from flask import Flask, request, jsonify
import json
from ultralight import compute_energy
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/results.json')

# Ensure results.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    mass = float(data['mass'])
    energy = compute_energy(mass)

    # Load current results
    with open(DATA_FILE, 'r') as f:
        results = json.load(f)

    # Append new result
    results.append({'mass': mass, 'energy': energy})
    with open(DATA_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    return jsonify({'energy': energy})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
