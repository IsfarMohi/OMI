from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        # Retrieve query parameters
        query_params = request.args.to_dict()
        print("Query Params:", query_params)
        return jsonify({
            "message": "This is a GET request!",
            "received_data": query_params
        })

    if request.method == 'POST':
        # Ensure the client sends JSON data with Content-Type: application/json
        try:
            json_data = request.json  # Extract JSON data
            print("JSON Data:", json_data)
            return jsonify({
                "message": "This is a POST request!",
                "received_data": json_data
            })
        except Exception as e:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
