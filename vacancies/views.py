from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from vacancies.models import Vacancy, Specialty, Company


class IndexView(ListView):
    model = Company
    template_name = 'index.html'
    context_object_name = 'companies'
    queryset = Company.objects.prefetch_related('vacancies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects. \
            prefetch_related('vacancies')
        return context


class VacancyListView(ListView):
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    queryset = Vacancy.objects. \
        select_related('specialty'). \
        select_related('company')
    extra_context = {'title': 'Все вакансии'}


class VacancyBySpecialtyListView(ListView):
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    # extra_context = self.get_specialty()

    def get_queryset(self):
        self.specialty = get_object_or_404(Specialty,
                                           code=self.kwargs['specialty'])
        return Vacancy.objects.filter(specialty=self.specialty). \
            select_related('specialty'). \
            select_related('company')

    def get_specialty(self):
        return {'specialty': get_object_or_404(Specialty,
                                           code=self.kwargs['specialty'])}


def companie_view(request):
    return HttpResponse("companie_view.")


def vacancie_view(request):
    return HttpResponse("vacancie_view.")
