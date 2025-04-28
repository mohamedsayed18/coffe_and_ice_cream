# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    return JsonResponse({'token': 'abc123'})