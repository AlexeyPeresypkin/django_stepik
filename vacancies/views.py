from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from vacancies.forms import CompanyForm, ApplicationForm
from vacancies.models import Vacancy, Specialty, Company, Application


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


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'company-create.html'
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vacancies:my_company_view')


# class VacancyView(DetailView):
#     model = Vacancy
#     template_name = 'vacancy.html'
#     context_object_name = 'vacancy'


class VacancyView(View):

    def get(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get('pk'))
        return render(request, 'vacancy.html', {'vacancy': vacancy})

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        pk = self.kwargs.get('pk')
        vacancy = get_object_or_404(Vacancy, pk=pk)
        user = self.request.user
        if not user.is_authenticated:
            messages.info(request, 'Необходимо войти чтобы отправить отклик')
            return redirect('login')
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.vacancy = vacancy
            application.save()
            return reverse('vacancies:vacancy_send_view', kwargs={'pk': pk})
        return render(request, 'vacancy.html', {'form': form})

# class DataView(LoginRequiredMixin, View):
#
#     @login_required
#     def post(self, request, *args, **kwargs):
#         form = ApplicationForm(request.POST)
#         vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get('pk'))
#         user = self.request.user
#         form.user = user
#         form.vacancy = vacancy
#         print(form.is_valid())
#         return render(request, 'index.html')


class VacancySendView(DetailView):
    model = Vacancy
    template_name = 'sent.html'
    context_object_name = 'vacancy'


class CompanyEditView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user).first()
        if company:
            form = CompanyForm(instance=company)
        else:
            form = CompanyForm()
        return render(
            request,
            'company-edit.html',
            {'form': form, 'company': company}
        )

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user).first()
        form = CompanyForm(
            request.POST or None,
            request.FILES or None,
            instance=company
        )
        if form.is_valid():
            form.save()
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
