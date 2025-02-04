from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number or not number.isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)

    response = {
        "number": number,
        "message": "Basic setup complete!"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
