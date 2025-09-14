from flask import Flask, request, jsonify
import subprocess
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.fortran_db
collection = db.results

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    mass = float(data['mass'])

    # Call Fortran executable
    process = subprocess.Popen(
        ['./fortran/ultralight', str(mass)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if stderr:
        return jsonify({'error': stderr.decode()}), 500

    # Extract energy from Fortran output
    energy = float(stdout.decode().strip().split()[-1])

    # Store in MongoDB
    collection.insert_one({'mass': mass, 'energy': energy})

    return jsonify({'energy': energy})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
