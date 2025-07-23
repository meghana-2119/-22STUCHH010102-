import random
import string
from datetime import datetime, timedelta
import re

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def validate_url(url):
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([\da-z.-]+)\.([a-z.]{2,6})'  # domain
        r'([/\w .-]*)*/?$'  # path
    )
    return re.match(regex, url) is not None

def get_expiry_datetime(validity):
    return datetime.utcnow() + timedelta(minutes=int(validity))
