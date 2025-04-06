from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import mysql.connector
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the CNN model once
model = load_model('model/bone_fracture_model.h5')

# Define Flask blueprint
routes = Blueprint('routes', __name__)

#  Health check route
@routes.route('/test', methods=['GET'])
def test():
    return " Routes are working!"

#  SIGNUP
@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

#  LOGIN
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

#  PREDICT
@routes.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 🔍 Step 1: Preprocess Image
        image = Image.open(file).convert('RGB')
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        print(" Image shape after preprocessing:", image.shape)

        # 🤖 Step 2: Predict using model
        prediction = model.predict(image)
        print(" Raw prediction output:", prediction)

        predicted_class = int(np.argmax(prediction[0]))
        print(" Predicted class index:", predicted_class)

        #  Step 3: Class labels & recommendations
        labels = ['No Fracture', 'Minor Fracture', 'Major Fracture']
        recommendations = {
            'No Fracture': '✅ Your bone is healthy. No treatment needed.',
            'Minor Fracture': ' 🟡 Use a splint or cast. Follow up with your doctor.',
            'Major Fracture': '🛑 Surgery might be required. Consult an orthopedic specialist immediately.'
        }

        # Check if predicted index is within range
        if predicted_class >= len(labels):
            return jsonify({'error': 'Prediction index out of label range'}), 500

        result = labels[predicted_class]
        recommendation = recommendations[result]

        #  Step 4: Return Prediction + Recommendation
        return jsonify({
            'prediction': result,
            'recommendation': recommendation
        }), 200

    except Exception as e:
        print(" Error during prediction:", str(e))
        return jsonify({'error': str(e)}), 500

