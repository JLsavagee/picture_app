from flask import Flask
from flask_cors import CORS
from routes.image_routes import image_blueprint
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://editor.team-cards.de"}})

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
