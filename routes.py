from flask import Blueprint, request, jsonify, redirect
from models import get_db, get_url_by_shortcode, create_short_url, get_stats, log_click
from utils import generate_shortcode, validate_url, get_expiry_datetime
from datetime import datetime

shorturl_bp = Blueprint('shorturl', __name__)

@shorturl_bp.route('/shorturls', methods=['POST'])
def create_shorturl():
    data = request.get_json()
    url = data.get('url')
    validity = data.get('validity', 30)
    shortcode = data.get('shortcode')
    if not url or not validate_url(url):
        return jsonify({'error': 'Invalid URL'}), 400
    if shortcode and get_url_by_shortcode(shortcode):
        return jsonify({'error': 'Shortcode already exists'}), 409
    if not shortcode:
        shortcode = generate_shortcode()
    expiry = get_expiry_datetime(validity)
    try:
        create_short_url(url, shortcode, expiry)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({
        'shortLink': f"http://localhost:5000/{shortcode}",
        'expiry': expiry.isoformat() + 'Z'
    }), 201

@shorturl_bp.route('/<shortcode>', methods=['GET'])
def redirect_shorturl(shortcode):
    url_data = get_url_by_shortcode(shortcode)
    if not url_data:
        return jsonify({'error': 'Shortcode not found'}), 404
    if datetime.utcnow() > url_data['expiry']:
        return jsonify({'error': 'Shortcode expired'}), 410
    log_click(shortcode, request)
    return redirect(url_data['originalURL'])

@shorturl_bp.route('/shorturls/<shortcode>', methods=['GET'])
def get_shorturl_stats(shortcode):
    stats = get_stats(shortcode)
    if not stats:
        return jsonify({'error': 'Shortcode not found'}), 404
    return jsonify(stats), 200
