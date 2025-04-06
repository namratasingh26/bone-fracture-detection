from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)

# Optional: Print registered routes for debugging
for rule in app.url_map.iter_rules():
    print(f"Route: {rule}, Methods: {rule.methods}")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
