from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from vacancies.forms import CompanyForm, ApplicationForm, VacancyForm
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
        specialty = get_object_or_404(Specialty,
                                      code=self.kwargs['specialty'])
        return Vacancy.objects.filter(specialty=specialty). \
            select_related('specialty'). \
            select_related('company')


class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancy-create.html'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vacancies:my_company_vacancies_view')


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


class VacancyView(View):

    def get(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get('pk'))
        return render(request, 'vacancy.html', {'vacancy': vacancy})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        vacancy = get_object_or_404(Vacancy, pk=pk)
        user = self.request.user
        form = ApplicationForm(request.POST, vacancy=vacancy, user=user)
        if not user.is_authenticated:
            messages.info(request, 'Необходимо войти чтобы отправить отклик')
            return redirect('login')
        if form.is_valid():
            form.save()
            return render(request, 'sent.html', {'vacancy': vacancy})
        return render(request, 'vacancy.html', {'form': form})


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
        return render(
            request,
            'company-edit.html',
            {
                'form': form,
                'message': 'Информация о компании обновлена',
                'company': company,
            }
        )


class MyCompanyVacanciesView(LoginRequiredMixin, ListView):
    template_name = 'vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = Vacancy.objects. \
            filter(company=self.request.user.company). \
            prefetch_related('applications')
        return queryset


class MyCompanyVacancyView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get('pk'))
        form = VacancyForm(instance=vacancy)
        applications = vacancy.applications
        return render(
            request,
            'vacancy-edit.html',
            {
                'form': form,
                'applications': applications,
                'vacancy': vacancy
            }
        )

    def post(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=kwargs.get('pk'))
        if vacancy.company.owner != request.user:
            return redirect('vacancies:my_company_view')
        form = VacancyForm(request.POST or None, instance=vacancy)
        if form.is_valid():
            form.save()
        return render(
            request,
            'vacancy-edit.html',
            {
                'form': form,
                'message': 'Вакансия обновлена'
            }
        )


class ApplicationsView(ListView):
    model = Application
    template_name = 'applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        applications = Application.objects. \
            filter(vacancy_id=self.kwargs.get('pk'))
        return applications


def about(request):
    return render(request, 'about.html', {'title': 'about'})


def search(request):
    q = request.GET.get('q')
    if q:
        vacancies = Vacancy.objects. \
            filter(Q(title__icontains=q) | Q(description__icontains=q)). \
            distinct(). \
            select_related('company')
        print(vacancies)
        return render(request, 'search.html', {'vacancies': vacancies})
    return render(request, 'search.html')


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
