from flask import Flask
from flask_cors import CORS
from routes.image_routes import image_blueprint
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

if os.getenv("FLASK_ENV") == "development":
    load_dotenv(".env.development")
else:
    load_dotenv(".env.production")

FLASK_ENV = os.getenv("FLASK_ENV")
API_URL = os.getenv("API_URL")
FLASK_APP_HOST = os.getenv("FLASK_APP_HOST")
FLASK_APP_PORT = os.getenv("FLASK_APP_PORT")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

# Print to confirm environment
print(f"Running in {FLASK_ENV} mode with API URL {API_URL} and CORS {CORS_ORIGINS} ")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

# Set maximum allowed payload to 20 megabytes
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

# Register Blueprints
app.register_blueprint(image_blueprint, url_prefix='/')

# Handle 'RequestEntityTooLarge' exception
@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(e):
    return {'error': 'File too large'}, 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
