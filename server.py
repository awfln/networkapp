from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)

# File to store client system specs
filename = 'system_specs.json'

# Function to load stored specs from the file
def load_specs():
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save new specs to the file
def save_specs(specs):
    with open(filename, 'w') as f:
        json.dump(specs, f, indent=4)

# Route to receive specs from clients
@app.route('/receive-specs', methods=['POST'])
def receive_specs():
    data = request.get_json()  # Get the incoming JSON data
    if data:
        # Add timestamp for when the specs are received
        data['timestamp'] = str(datetime.datetime.now())
        
        # Add the received specs to the file
        specs_list = load_specs()
        specs_list.append(data)
        save_specs(specs_list)
        
        # Display the received specs (optional)
        print(f"Received specs: {data}")
        
        return jsonify({"success": True, "message": "Specs received!"}), 200
    else:
        return jsonify({"success": False, "error": "No specs provided"}), 400

# Route to view all specs in real-time
@app.route('/view-specs', methods=['GET'])
def view_specs():
    specs_list = load_specs()
    return jsonify(specs_list), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
