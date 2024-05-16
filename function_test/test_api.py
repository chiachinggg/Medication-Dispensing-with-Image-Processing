# test_views.py
from django.test import TestCase
from rest_framework.test import APIClient

class TestAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_hello_world(self):
        response = self.client.get('/api/test_api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Hello, world!')

    def test_post_request(self):
        data = {'id': 1, 'name': 'John Doe'}
        response = self.client.post('/api/test_api_post/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_store_image(self):
        # Assuming you have an image file named 'test_image.jpg' in the same directory as this test file
        with open('test_image.jpg', 'rb') as image_file:
            data = {
                'image': image_file.read(),
                'filename': 'test_image.jpg'
            }
            response = self.client.post('/api/store_image/', data, format='multipart')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of your store_image endpoint

