from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/sign_up')
def index():
    return render_template('sign_up.html')

@app.route('/main', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Replace this with actual authentication logic
    if username == 'admin' and password == 'password':
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials."}), 401

if __name__ == '__main__':
    app.run(debug=True)
