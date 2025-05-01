from django.test import TestCase
import json

from . import models


class TestApi(TestCase):
    def setUp(self):
        models.SystemSettings.objects.create(settings='system_state', value='Log in')

    def get_system_state(self) -> str:
        url = 'http://localhost:8000/myapi/state/'
        response = self.client.get(url)
        response_data = json.loads(response.content)
        return response_data['state']
    
    def set_system_state(self, state: str) -> None:
        system_state = models.SystemSettings.objects.get(settings='system_state')
        system_state.value = state
        system_state.save()

    def test_login_success(self):
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'admin',
            'password': '1234'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_system_state(), 'Dashboard')

    def test_login_failure(self):
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'admin',
            'password': 'secret'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.get_system_state(), 'Log in')

    def test_change_system_state(self):
        self.set_system_state('Dashboard')

        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Item Details'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['new_state'], 'Item Details')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_system_state(), 'Item Details')

    def test_change_system_state_wrong_transition(self):
        self.set_system_state('Item Details')

        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Config'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

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
