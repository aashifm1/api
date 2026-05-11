from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database
users = {}

# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "User API is running"
    })


# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


# Get single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    if user_id not in users:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(users[user_id]), 200


# Create user
@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    # Validate request
    if not data:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    # Create new user ID
    user_id = len(users) + 1

    new_user = {
        "id": user_id,
        "name": name,
        "email": email
    }

    users[user_id] = new_user

    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


# Delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    if user_id not in users:
        return jsonify({
            "error": "User not found"
        }), 404

    deleted_user = users.pop(user_id)

    return jsonify({
        "message": "User deleted",
        "user": deleted_user
    }), 200


if __name__ == "__main__":
    app.run(debug=True)