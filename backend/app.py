from flask import Flask
from flask_cors import CORS
from backend.routes.image_routes import image_blueprint

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(image_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)