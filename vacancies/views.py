from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from vacancies.forms import CompanyForm
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
    extra_context = {'header': 'Все вакансии'}


class VacancyBySpecialtyListView(ListView):
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        self.specialty = get_object_or_404(Specialty,
                                           code=self.kwargs['specialty'])
        return Vacancy.objects.filter(specialty=self.specialty). \
            select_related('specialty'). \
            select_related('company')


class CompanyView(DetailView):
    template_name = 'company.html'
    context_object_name = 'company'
    queryset = Company.objects. \
        prefetch_related('vacancies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Company.objects.get(pk=self.kwargs['pk'])
        return context


class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company-create.html'
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vacancies:my_company_view')


class VacancyView(DetailView):
    model = Vacancy
    template_name = 'vacancy.html'
    context_object_name = 'vacancy'


class VacancySendView(DetailView):
    model = Vacancy
    template_name = 'sent.html'


class CompanyEditView(View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user).values()[0]
        form = CompanyForm(company)
        print(company)
        print(form.is_bound)
        print(form.is_valid())
        print(form.instance.name)
        return render(request, 'company-edit.html', {'form': form})


class MyCompanyVacanciesView(ListView):
    model = Vacancy


class MyCompanyVacancyView(DetailView):
    model = Vacancy


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
