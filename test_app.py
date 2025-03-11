import unittest
from app import app
import json

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    # ✅ Test Home Route
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to PubMed Fetcher API!", response.data)
    
    # ✅ Test Get Papers Route
    def test_get_papers(self):
        response = self.app.get('/papers')
        self.assertIn(response.status_code, [200, 404])  # Accept 404 if no data available
        if response.status_code == 200:
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Papers exported to CSV successfully')

    # ✅ Test Search Papers Route
    def test_search_papers(self):
        response = self.app.get('/search?query=cancer')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = response.get_json()
            self.assertIsInstance(data, list)
            if data:
                self.assertIn('ID', data[0])
                self.assertIn('Title', data[0])
            else:
                print("No papers found for the query.")

    # ✅ Test Get Single Paper (Valid ID)
    def test_get_single_paper(self):
        response = self.app.get('/paper/40064631')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = response.get_json()
            self.assertIn('ID', data)
            self.assertIn('Title', data)
            self.assertIn('Authors', data)
            self.assertIn('Publication Date', data)

    # ✅ Test Get Single Paper (Invalid ID)
    def test_get_invalid_paper(self):
        response = self.app.get('/paper/99999999')  # Non-existing ID
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Paper not found')

    # ✅ Test Export as JSON
    def test_export_json(self):
        response = self.app.get('/export/json')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
        else:
            data = response.get_json()
            self.assertIn('error', data)

    # ✅ Test Export as CSV
    def test_export_csv(self):
        response = self.app.get('/export/csv')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertEqual(response.headers['Content-Type'], 'text/csv; charset=utf-8')
            content = response.data.decode('utf-8')
            self.assertIn('ID,Title,Authors,Journal,Publication Date', content)
        else:
            data = response.get_json()
            self.assertIn('error', data)

    # ✅ Test Test Fetch Route
    def test_test_fetch(self):
        response = self.app.get('/test_fetch')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = response.get_json()
            self.assertIsInstance(data, list)
            if data:
                self.assertIn('ID', data[0])
                self.assertIn('Title', data[0])
            else:
                print("No papers fetched.")

if __name__ == '__main__':
    unittest.main()
