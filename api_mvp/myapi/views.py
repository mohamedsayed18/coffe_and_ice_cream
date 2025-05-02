from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from enum import Enum
import json
from dataclasses import asdict
from typing import Optional

from . import models


item_control_allowed: bool = False
user_name = 'admin'
password = '1234'

class state(Enum):
    INIT = 'init'
    RUN = 'run'
    PAUSE = 'pause'
    STOP = 'stop'

transition_states = {
    'Log in': [],
    'Dashboard': ['Log in', 'Config', 'Item Details', 'Item Control'],
    'Config': ['Dashboard'],
    'Item Details': ['Dashboard', 'Item Control'],
    'Item Control': ['Dashboard', 'Item Details'],
}

def get_system_state() -> str:
    state_obj = models.SystemSettings.objects.get(settings='system_state')
    return state_obj.value

def set_system_state(new_state: str) -> None:
    system_state, _ = models.SystemSettings.objects.get_or_create(settings='system_state')
    system_state.value = new_state
    system_state.save()

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login_name = data.get('username')
        login_password = data.get('password')
        if login_name == user_name and login_password == password:
            set_system_state('Dashboard')
            return JsonResponse({'result': 'successfully logged in'})
        else:
            return JsonResponse({'error': 'Failed login, wrong username or password'}, status=401)

@csrf_exempt
def change_system_state(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        new_state = body.get('new_state')
        if new_state in transition_states[get_system_state()]:
            if new_state == 'Item Control' and not item_control_allowed:
                return JsonResponse({'error': f'Transition to Item Control Denied'}, status=409)
            set_system_state(new_state)
            return JsonResponse({'new_state': get_system_state()})
        else:
            return JsonResponse({'error': f'Cannot transition from {get_system_state()} to {new_state}'}, status=409)

    elif request.method == 'GET':
        return JsonResponse({'state': get_system_state()})

def filter_items(items_list: list, filter: str) -> list:
    filtered_items: list = []
    for item in items_list:
        if item['state'] == filter:
            filtered_items.append(item)
    return filtered_items

def create_item(id: str, description: str) -> None:
    models.Items.objects.create(id=id, description=description, state=state.INIT.value, date=datetime.now().date().isoformat())

def get_item(id: str, items_list: list) -> Optional[dict]:
    for i in items_list:
        if i['id'] == id:
            return JsonResponse(i)
    return None

@csrf_exempt
def change_item_state(request, item_id:str):
    if request.method == 'PUT':
        if get_system_state() == 'Item Control':
            data = json.loads(request.body)
            new_state = data.get('state')
            item_obj = models.Items.objects.get(id=item_id)
            item_obj.state = new_state
            item_obj.save()
            return JsonResponse({'result': f'item {item_id} state is {new_state}'})

@csrf_exempt
def handle_items(request):
    if request.method == 'GET':
        all_items = models.Items.objects.all()
        items_list = [model_to_dict(item) for item in all_items]
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        sort_order = request.GET.get('sort')
        id = request.GET.get('id')
        if id:
            if get_system_state() == 'Item Details':
                return get_item(id, items_list)
            else:
                return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)

        if get_system_state() == 'Dashboard':
            if sort_order:
                reverse = sort_order == 'desc'
                items_list.sort(key=lambda item: item['created_at'], reverse=reverse)

            state_filter = request.GET.get('state')
            if state_filter:
                items_list = filter_items(items_list, state_filter)
            paginator = Paginator(items_list, page_size)
            page_obj = paginator.get_page(page_number)

            data = {
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'result': [item for item in page_obj.object_list]
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)

    elif request.method == 'POST':
        if get_system_state() == 'Dashboard':
            body = json.loads(request.body)
            id = body.get('id')
            description = body.get('description')
            create_item(id, description)
            return JsonResponse({'new item added': 'success'})
        else:
            return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)

def update_credentials(new_username:str, new_password:str) -> None:
    global user_name
    global password
    if new_username:
        user_name = new_username
    if new_password:
        password = new_password

@csrf_exempt
def update_user(request):
    if get_system_state() == 'Config':
        if request.method == 'PUT':
            try:
                data = json.loads(request.body)
                new_username = data.get('username')
                new_password = data.get('password')
                update_credentials(new_username, new_password)
                set_system_state('Log in')
                return JsonResponse({'message': 'User Credentials updated'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def item_control_access(request) -> None:
    global item_control_allowed
    if get_system_state() == 'Config':
        if request.method == 'PUT':
            data = json.loads(request.body)
            item_control_allowed = data.get('allowed')
            set_system_state('Log in')
            return JsonResponse({'message': f'Access to Item Control set to {item_control_allowed}'})
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:
        return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)
