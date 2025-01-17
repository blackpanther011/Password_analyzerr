from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def check_password_strength(password):
    length_criteria = len(password) >= 8
    digit_criteria = re.search(r"\d", password) is not None
    uppercase_criteria = re.search(r"[A-Z]", password) is not None
    lowercase_criteria = re.search(r"[a-z]", password) is not None
    symbol_criteria = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

    score = sum([length_criteria, digit_criteria, uppercase_criteria, lowercase_criteria, symbol_criteria])

    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    elif score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    suggestions = []
    if not length_criteria:
        suggestions.append("Make your password at least 8 characters long.")
    if not digit_criteria:
        suggestions.append("Include at least one digit.")
    if not uppercase_criteria:
        suggestions.append("Include at least one uppercase letter.")
    if not lowercase_criteria:
        suggestions.append("Include at least one lowercase letter.")
    if not symbol_criteria:
        suggestions.append("Include at least one special character (e.g., !@#$%^&*).")

    return {"strength": strength, "suggestions": suggestions}

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get("password")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    result = check_password_strength(password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)