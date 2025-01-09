import unittest
import json
from app import app, url_mapping

class URLShortenerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        url_mapping.clear()

    def test_shorten_valid_url(self):
        response = self.app.post('/shorten', json={'url': 'http://example.com'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('short_url', data)

    def test_shorten_invalid_url(self):
        response = self.app.post('/shorten', json={'url': 'not-a-valid-url'})
        self.assertEqual(response.status_code, 400)

    def test_redirect_valid_short_url(self):
        short_code = 'abc123'
        url_mapping[short_code] = 'http://example.com'
        response = self.app.get(f'/{short_code}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://example.com')

    def test_redirect_invalid_short_url(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_uniqueness_of_short_url(self):
        response1 = self.app.post('/shorten', json={'url': 'http://example1.com'})
        response2 = self.app.post('/shorten', json={'url': 'http://example2.com'})
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        self.assertNotEqual(data1['short_url'], data2['short_url'])

if __name__ == '__main__':
    unittest.main()
