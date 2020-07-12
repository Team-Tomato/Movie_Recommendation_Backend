import unittest
import json
from app import app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True


    def tearDown(self):
        pass

      
# Testing Main Route
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Welcome to Team-Tomato movie recommendation system')


    # Check for Negative Response
    def test_index1(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='application/json')
        self.assertEqual(response.status_code, 500)

    
#  Testing Cosine Similarity Model
    #Checking Response Status Code is 200
    def test_cosineSimilarity(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/cosine', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #Checking for Negative Response
    def test_cosineSimilarity1(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/cosine/1', content_type='application/json')
        self.assertEqual(response.status_code, 500)


# Testing Genre Based Route
    #Checking Response Status Code is 200
    def test_genreBased(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/genre', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #Checking  for Negative Response 
    def test_genreBased1(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/genre/Action', content_type='application/json')
        self.assertEqual(response.status_code, 500)


# Testing Rating Based Route
    #Checking Response Status Code is 200
    def test_ratingBased(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/rating', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #Checking for Negative Response 
    def test_ratingBased1(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/movie/rating/9', content_type='application/json')
        self.assertEqual(response.status_code, 500)




if __name__ == '__main__':
    unittest.main(verbosity=2)
