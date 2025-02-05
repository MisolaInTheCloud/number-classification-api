import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n == 2:
        return True  # 2 is the only even prime number
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get("text", "No fact available.")
    except requests.RequestException as e:
        print(f"Error fetching fun fact: {e}")  # Log the error
        return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Check if the input is valid
    if not number or not number.isdigit() or int(number) < 0:
        return jsonify({"error": "Invalid input. Please provide a non-negative integer."}), 400

    number = int(number)

    properties = []

    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)
