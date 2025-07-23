import logging
from flask import request

class CustomLogger(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        with open('url_shortener.log', 'a') as f:
            f.write(log_entry + '\n')

def setup_custom_logger(app):
    handler = CustomLogger()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.path} - {request.remote_addr}")

    @app.after_request
    def log_response(response):
        app.logger.info(f"Response: {response.status_code} {request.path}")
        return response
