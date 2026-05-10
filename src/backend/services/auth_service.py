# Blueprint lets us keep auth routes in this file instead of putting everything in app.py
# Lets flask know these routes exist
import bcrypt
from flask import Blueprint, jsonify, request
from boto3.dynamodb.conditions import Attr

from models.user import User

def create_auth_blueprint(table, is_rate_limited):
    auth_bp = Blueprint("auth", __name__)

    #create new user endpoint
    @auth_bp.route("/api/create_account", methods=["POST"])
    def create_account():
        """Create a new user account.
        
        Request Body:
            {
                "username": str (required) - Unique username
                "password": str (required) - User password 
            }
        
        Returns:
            201 - Account created successfully:
                {
                    "message": str - Success message
                    "user_id": str - Unique user ID
                    "username": str - Username
                }
            400 - Bad request (empty data, missing fields, or username already exists)
            429 - Too many requests (rate limited)
        
        """
        data = request.get_json()   #gets json data

        #error check if request is empty
        if not data:
            return jsonify({"error": "No data"}), 400

        #gets username and pw from json
        username = data.get("username")
        password = data.get("password")

        #makes sure username and pw are given
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        #rate limit account create attempts
        if is_rate_limited(username):
            return jsonify({"error": "Too many request"}), 429

        #checks if username already exists in DynamoDB
        response = table.scan(FilterExpression=Attr("username").eq(username))

        #if username does already exist, return error
        if response.get("Items"):   #checks if Items has sometihng inside
            return jsonify({"error": "Username already exists"}), 400

        #bcrypt requires bytes
        password_bytes = password.encode("utf-8")
        #hash pw with salt
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        #decodes hashed pw to store in DynamoDB as string
        hashed_password = hashed_password.decode("utf-8")

        #create new User object with hashed pw; diary is empty rated games
        new_user = User.from_dict({
            "username": username,
            "password": hashed_password,
            "diary": []
        })

        #saves the new user to DynamoDB
        table.put_item(Item=new_user.to_dict())

        #sends back account info except pw
        return jsonify({
            "message": "Account created successfully",
            "user_id": new_user.user_id,
            "username": new_user.username,
        }), 201

    #login endpoint
    @auth_bp.route("/api/login", methods=["POST"])
    def login():
        """Authenticate user and return user info.
        
        Request Body:
            {
                "username": str (required) - Registered username
                "password": str (required) - User password
            }
        
        Returns:
            200 - Login successful:
                {
                    "message": str - Success message
                    "user_id": str - Unique user ID
                    "username": str - Username
                    "diary": list - User's rated games
                }
            400 - Bad request (empty data or missing fields)
            401 - Unauthorized (invalid password)
            404 - User not found (invalid username)
            429 - Too many requests (rate limited)
        
        """
        data = request.get_json()   #gets json data
        #error check for empty body
        if not data:
            return jsonify({"error": "No data"}), 400

        #gets username and password from json data
        username = data.get("username")
        password = data.get("password")

        #make sure both username and pw is entered
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        #rate limits login attempts per username
        if is_rate_limited(username):
            return jsonify({"error": "Too many requests"}), 429

        #searches DynamoDB specific username
        response = table.scan(FilterExpression=Attr("username").eq(username))

        #gets the matching user from DB
        users = response.get("Items", [])

        #give error if username doesn't exist in DB
        if not users:
            return jsonify({"error": "Invalid username or password"}), 404

        #converts DynamoDB user dict to User object
        user = User.from_dict(users[0])

        #encode inputted pw to bytes
        password_bytes = password.encode("utf-8")
        #encode stored DB pw to bytes
        stored_password = user.password.encode("utf-8")

        #checks if the inputted pw matches the stored hashed pw
        if not bcrypt.checkpw(password_bytes, stored_password):
            return jsonify({"error": "Invalid username or password"}), 401

        #login successful, send back the user's info to frontend
        return jsonify({
            "message": "Login successful",
            "user_id": user.user_id,
            "username": user.username,
            "diary": user.diary
        }), 200

    #maybe make a logout endpoint here

    #returns the blueprint so app.py for Flask
    return auth_bp












