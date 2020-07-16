import unittest
import json
from app import app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def tearDown(self):
        pass

      
# Testing Main Route
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Welcome to Team-Tomato movie recommendation system')

    
#  Testing Cosine Similarity Model
    #Checking Response Status Code is 200
    def test_cosineSimilarity(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/cosine', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #Checking for Response Data
    def test_cosine(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/cosine', content_type='application/json')
        self.assertEqual(b'No results found', response.data)
   
# Testing Genre Based Route
    #Checking Response Status Code is 200
    def test_genreBased(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/genre', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #Checking for Response Data
    def test_genre(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/genre', content_type='application/json')
        self.assertTrue(b'no attribute'in response.data)

   

# Testing Rating Based Route
    #Checking Response Status Code is 200
    def test_ratingBased(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/rating', content_type='application/json')
        self.assertEqual(response.status_code, 200)

   



if __name__ == '__main__':
    unittest.main(verbosity=2)
