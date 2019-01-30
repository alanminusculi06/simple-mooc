from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    template_name = 'home.html'
    return render(request, template_name)

def contato(request):
    template_name = 'contato.html'
    return render(request, template_name)
