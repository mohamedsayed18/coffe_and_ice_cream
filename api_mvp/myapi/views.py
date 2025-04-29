# from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import json

from . import items

system_state = 'Log in'

transition_states = {
    'Log in': ['Dashboard'],
    'Dashboard': ['Log in', 'Config', 'Item Details', 'Item Control'],
    'Config': ['Dashboard'],
    'Item Details': ['Dashboard', 'Item Control'],
    'Item Control': ['Dashboard', 'Item Details'],
}

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    if system_state == 'dashboard':
        return JsonResponse({'token': 'abc123'})
    else:
        return JsonResponse({'token': '789'})

def change_system_state(request):
    global system_state
    if request.method == 'POST':
        body = json.loads(request.body)
        new_state = body.get('new_state')
        if new_state in transition_states[system_state]:
            system_state = new_state
            return JsonResponse({'new_state': system_state})
        else:
            return JsonResponse({'error': f'Cannot transition from {system_state} to {new_state}'}, status=409)

    elif request.method == 'GET':
        return JsonResponse({'state': system_state})

def filter_items(items_list: list, filter: str) -> list:
    filtered_items: list = []
    for item in items_list:
        if item['state'] == filter:
            filtered_items.append(item)
    return filtered_items

def handle_items(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 3)
    state_filter = request.GET.get('state')
    all_items = items.subscriptions
    if state_filter:
        all_items = filter_items(items.subscriptions, state_filter)
    paginator = Paginator(all_items, page_size)
    page_obj = paginator.get_page(page_number)

    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'reult': [item for item in page_obj.object_list]
    }
    return JsonResponse(data)