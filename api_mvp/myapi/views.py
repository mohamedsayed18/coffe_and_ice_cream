from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from dataclasses import asdict

from . import items
from . import models


item_control_allowed: bool = False

# TODO Make system states Enum
transition_states = {
    'Log in': ['Dashboard'],
    'Dashboard': ['Log in', 'Config', 'Item Details', 'Item Control'],
    'Config': ['Dashboard'],
    'Item Details': ['Dashboard', 'Item Control'],
    'Item Control': ['Dashboard', 'Item Details'],
}

all_items = items.subscriptions

def get_system_state() -> str:
    state_obj = models.SystemSettings.objects.get(settings='system_state')
    return state_obj.value

def set_system_state(new_state: str) -> None:
    system_state, _ = models.SystemSettings.objects.get_or_create(settings='system_state')
    system_state.value = new_state
    system_state.save()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username == 'admin' and password == '1234':
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

def create_item(id: str, description: str) -> dict:
    return asdict(items.Item(id, description, items.state.INIT.value, datetime.now().date().isoformat()))

def get_item(id: str)->dict:
    global all_items
    for i in all_items:
        if i['id'] == id:
            return JsonResponse({'item': i})

@csrf_exempt
def change_item_state(request, item_id:str):
    global all_items
    if request.method == 'PUT':
        if get_system_state() == 'Item Control':
            data = json.loads(request.body)
            state = data.get('state')
            for i in all_items:
                if i['id'] == item_id:
                    i['state'] = state # TODO USE enum to avoid typo
                    return JsonResponse({'result': f'item {i['id']} state is {state}'})

@csrf_exempt
def handle_items(request):
    global all_items
    if request.method == 'GET':
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        sort_order = request.GET.get('sort')
        id = request.GET.get('id')
        if id:
            if get_system_state() == 'Item Details':
                return get_item(id)
            else:
                return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)

        if get_system_state() == 'Dashboard':
            if sort_order:
                reverse = sort_order == 'desc'
                all_items.sort(key=lambda item: item['created_at'], reverse=reverse)

            state_filter = request.GET.get('state')
            if state_filter:
                all_items = filter_items(items.subscriptions, state_filter)
            paginator = Paginator(all_items, page_size)
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
            all_items.append(create_item(id, description))
            return JsonResponse({'new item added': 'success'})
        else:
            return JsonResponse({'error': f'Operation is not allowed in {get_system_state()} state'}, status=409)

def update_credentials():
    pass    #TODO

@csrf_exempt
def update_user(request):
    if get_system_state() == 'Config':
        if request.method == 'PUT':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                update_credentials()
                set_system_state('Log in')
                return JsonResponse({'message': 'User updated'}, status=200)
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
