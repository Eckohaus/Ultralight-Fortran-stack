from flask import Flask, request, jsonify
import subprocess
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup (replace <username> and <password>)
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/fortran_db")
db = client.fortran_db
collection = db.results

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    mass = str(data['mass'])

    # Call Fortran executable
    process = subprocess.Popen(
        ['./fortran/ultralight', mass],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if stderr:
        return jsonify({'error': stderr.decode()}), 500

    energy = float(stdout.decode().strip().split()[-1])

    # Store input/output in MongoDB
    collection.insert_one({'mass': float(mass), 'energy': energy})

    return jsonify({'energy': energy})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
