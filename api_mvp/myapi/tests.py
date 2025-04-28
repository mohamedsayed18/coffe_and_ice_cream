from django.test import TestCase
import json


class TestApi(TestCase):
    def test_login_success(self):
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'admin',
            'password': 'secret'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
