from django.test import TestCase
import json

from . import models


class TestApi(TestCase):
    def setUp(self):
        models.SystemSettings.objects.create(settings='system_state', value='Log in')

    def test_login_success(self):
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'admin',
            'password': '1234'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        url = 'http://localhost:8000/myapi/state/'
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['state'], 'Dashboard')

    def test_login_failure(self):
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'admin',
            'password': 'secret'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

        url = 'http://localhost:8000/myapi/state/'
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['state'], 'Log in')

    def test_change_system_state(self):
        system_state = models.SystemSettings.objects.get(settings='system_state')
        system_state.value = 'Dashboard'
        system_state.save()

        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Item Details'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['new_state'], 'Item Details')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['state'], 'Item Details')

    def test_change_state_failure(self):
        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Item Details'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_add_item_failure(self):
        url = 'http://localhost:8000/myapi/items/'
        data = {'new_state': 'Item Details'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_add_item_in_correct_state(self):
        pass
