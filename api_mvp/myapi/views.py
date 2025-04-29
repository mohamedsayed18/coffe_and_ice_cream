# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from . import items

system_state = 'Login'

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
        system_state = new_state
        return JsonResponse({'new_state': system_state})

    elif request.method == 'GET':
        return JsonResponse({'state': system_state})

def handle_items(request):
    return JsonResponse({'items list': items.subscriptions})