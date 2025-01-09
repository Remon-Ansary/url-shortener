# URL Shortener Service

This project is a simple URL shortening service built with Python and Flask. It provides an API to shorten long URLs and redirect short URLs to their original destinations.

## Features

- Accepts a long URL and returns a unique short URL.
- Redirects from a short URL to the original long URL.
- Validates URLs to ensure they are properly formed.
- Generates unique short codes to avoid conflicts.
- In-memory storage using a Python dictionary for mapping URLs.

## Data Structure & Uniqueness Handling

**Data Structure:**  
The service uses a Python dictionary (`url_mapping`) to store mappings between short codes and long URLs. This structure provides:
- **Fast Lookup:** Constant average-time complexity for inserts and lookups.


**Approach to Short URL Uniqueness:**
- **Short Code Generation:** A 6-character alphanumeric string is generated randomly.
- **Collision Check:** After generating a new short code, the code checks if it already exists in the dictionary. If so, it generates a new code until a unique one is found.

## Installation

1. **Clone the Repository:**
   ```
   git clone https://github.com/Remon-Ansary/url-shortener.git
   cd url-shortener
    ```

2. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```
3 **Run the Application:**
    ```
    python app.py
    ```

## API Endpoints

1. **Shorten URL:**
   - **URL:** `http://localhost:5000/shorten`
   - **Method:** `POST`
   - **Request Body:** `{ "url": "https://www.example.com" }`
   - **Response:** `{ "short_url": "http://localhost:5000/abc123" }`