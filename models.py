from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'url_shortener')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collection: urls

def get_db():
    return db

def create_short_url(originalURL, shortcode, expiry):
    db.urls.insert_one({
        'originalURL': originalURL,
        'shortcode': shortcode,
        'createdAt': datetime.utcnow(),
        'expiry': expiry,
        'clicks': 0,
        'clickData': []
    })

def get_url_by_shortcode(shortcode):
    return db.urls.find_one({'shortcode': shortcode})

def log_click(shortcode, req):
    click = {
        'timestamp': datetime.utcnow(),
        'referrer': req.referrer,
        'location': req.headers.get('X-Geo-Location', 'Unknown')
    }
    db.urls.update_one({'shortcode': shortcode}, {
        '$inc': {'clicks': 1},
        '$push': {'clickData': click}
    })

def get_stats(shortcode):
    url = db.urls.find_one({'shortcode': shortcode})
    if not url:
        return None
    return {
        'clicks': url.get('clicks', 0),
        'originalURL': url['originalURL'],
        'createdAt': url['createdAt'].isoformat() + 'Z',
        'expiry': url['expiry'].isoformat() + 'Z',
        'clickData': url.get('clickData', [])
    }
