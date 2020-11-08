from django.http import HttpResponse
from django.shortcuts import render

def post_file(request):
    print('in here')
    return HttpResponse("<h1>Hello</h1")