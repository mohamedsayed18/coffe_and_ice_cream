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

    def count_items(self) -> int:
        self.set_system_state('Dashboard')
        url = 'http://localhost:8000/myapi/items/'
        response = self.client.get(url)
        response_data = json.loads(response.content)
        return response_data['count']

    def test_add_item_failure(self):
        items_count = self.count_items()
        self.set_system_state('Item Details')
        url = 'http://localhost:8000/myapi/items/'
        data = {'id': 'new_item', 'description': 'test item'}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        new_items_count = self.count_items()
        self.assertEqual(items_count, new_items_count)

    def test_add_item_success(self):
        items_count = self.count_items()
        self.set_system_state('Dashboard')
        url = 'http://localhost:8000/myapi/items/'
        data = {'id': 'nintendo', 'description': 'test item'}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        new_items_count = self.count_items()
        self.assertEqual(items_count+1, new_items_count)

    def test_change_item_state_success(self):
        # Add item
        self.set_system_state('Dashboard')
        url = 'http://localhost:8000/myapi/items/'
        data = {'id': 'nintendo', 'description': 'test item'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.set_system_state('Item Control')
        url = 'http://localhost:8000/myapi/items/nintendo/state'
        data = {'state': 'stop'}
        response = self.client.put(url,data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        self.set_system_state('Item Details')
        url = 'http://localhost:8000/myapi/items/?id=nintendo'
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['state'], 'stop')

    def test_item_control_failure(self):
        self.set_system_state('Dashboard')
        url = 'http://localhost:8000/myapi/item-control/'
        data = {'allowed': 'true'}
        respones = self.client.put(url, data=json.dumps(data))
        self.assertEqual(respones.status_code, 409)

    def test_item_control_success(self):
        self.set_system_state('Config')
        url = 'http://localhost:8000/myapi/item-control/'
        data = {'allowed': 'true'}
        respones = self.client.put(url, data=json.dumps(data))
        self.assertEqual(respones.status_code, 200)

        self.set_system_state('Dashboard')
        url = 'http://localhost:8000/myapi/state/'
        data = {'new_state': 'Item Control'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_system_state(), 'Item Control')

    def test_update_user_credentials(self):
        self.set_system_state('Config')
        url = 'http://localhost:8000/myapi/user/'
        data = {"username": "Hero", "password": "789"}
        response = self.client.put(url, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        # login with the new name and password
        url = 'http://localhost:8000/myapi/login/'
        data = {
            'username': 'Hero',
            'password': '789'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], 'successfully logged in')
        self.assertEqual(self.get_system_state(), 'Dashboard')
