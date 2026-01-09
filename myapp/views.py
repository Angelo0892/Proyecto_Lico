#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def contestame_telefonow(request):
    return HttpResponse("Hello contestame el telefo now")