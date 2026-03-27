from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data store
data_store = {"1": "Initial Item"}

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"method": "GET", "data": data_store}), 200

@app.route('/items', methods=['POST'])
def create_item():
    new_id = str(len(data_store) + 1)
    content = request.json.get('item', 'New Item')
    data_store[new_id] = content
    return jsonify({"method": "POST", "id": new_id, "added": content}), 201

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    if id in data_store:
        data_store[id] = request.json.get('item')
        return jsonify({"method": "PUT", "updated_id": id}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/items/<id>', methods=['PATCH'])
def patch_item(id):
    if id in data_store:
        # Dummy logic: just append " - patched"
        data_store[id] = f"{data_store[id]} - patched"
        return jsonify({"method": "PATCH", "patched_id": id}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    if id in data_store:
        del data_store[id]
        return jsonify({"method": "DELETE", "deleted_id": id}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    
    #Update the paths to your certificate and key files
    context = ('pq_server.crt', 'pq_server.key')
    
    print("Starting Post-Quantum Secure Server on https://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, ssl_context=context)
