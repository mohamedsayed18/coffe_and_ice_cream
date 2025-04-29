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

    def test_change_system_state(self):
        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Dashboard'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['new_state'], 'Dashboard')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['state'], 'Dashboard')
