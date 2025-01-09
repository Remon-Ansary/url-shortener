from flask import Flask, request, redirect, jsonify
import string, random, re

app = Flask(__name__)

# In-memory storage for mapping short codes to original URLs.
url_mapping = {}

# Base URL for constructing full short URLs.
BASE_URL = "http://localhost:5000/"

def generate_short_code(length=6):
    """
    Generate a random alphanumeric short code of a given length
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    """
    Validate the URL using regex.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'          # http:// or https://
        r'\w+(?:[\.-]\w+)*\.\w{2,}'    # domain
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Endpoint to create a short URL for a given long URL.
    """
    data = request.get_json()
    long_url = data.get('url')

    # Validate the provided URL
    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Check if this long URL has already been shortened
    for short_code, stored_url in url_mapping.items():
        if stored_url == long_url:
            return jsonify({"short_url": BASE_URL + short_code}), 200


    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    # Store the mapping in memory
    url_mapping[short_code] = long_url
    return jsonify({"short_url": BASE_URL + short_code}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_long_url(short_code):
    """
    Endpoint that redirects a short URL to its original long URL.
    """
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
