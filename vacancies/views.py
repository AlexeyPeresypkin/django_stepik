from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("index.")


def vacancies(request):
    return HttpResponse("vacancies.")


def cat_view(request):
    return HttpResponse("cat_view.")


def companie_view(request):
    return HttpResponse("companie_view.")



def vacancie_view(request):
    return HttpResponse("vacancie_view.")
