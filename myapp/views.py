from django.shortcuts import render,HttpResponse


def home(request):
    return HttpResponse("<h1>Hello World</h1>")
# Create your views here.
