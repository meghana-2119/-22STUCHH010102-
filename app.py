from flask import Flask
from routes import shorturl_bp
from logger import setup_custom_logger

app = Flask(__name__)
setup_custom_logger(app)

# Register blueprints
app.register_blueprint(shorturl_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
