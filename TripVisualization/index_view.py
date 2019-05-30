from django.shortcuts import render
from django.views.decorators import csrf

def index(request):  # index页面加载
    context = {}
    return render(request, 'index.html', context)