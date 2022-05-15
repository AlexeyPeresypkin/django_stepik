from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from vacancies.models import Vacancy, Specialty, Company


class IndexView(ListView):
    model = Company
    template_name = 'index.html'
    context_object_name = 'companies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        return context


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    queryset = Vacancy.objects. \
        select_related('specialty'). \
        select_related('company')


def cat_view(request):
    return HttpResponse("cat_view.")


def companie_view(request):
    return HttpResponse("companie_view.")


def vacancie_view(request):
    return HttpResponse("vacancie_view.")
