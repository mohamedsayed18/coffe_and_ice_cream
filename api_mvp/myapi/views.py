# from django.shortcuts import render
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

def handle_items(request):
    return JsonResponse({'items list': items.subscriptions})