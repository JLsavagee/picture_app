from flask import Flask
from flask_cors import CORS
from routes.image_routes import image_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://editor.team-cards.de"}})

# Register Blueprints
app.register_blueprint(image_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)