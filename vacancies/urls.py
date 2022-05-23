from django.urls import path

from vacancies.views import (
    VacancyView,
    IndexView,
    VacancyListView,
    VacancyBySpecialtyListView,
    CompanyView,
    MyCompanyVacanciesView,
    MyCompanyVacancyView,
    CompanyCreateView,
    CompanyEditView,
    ApplicationsView,
    VacancyCreateView,
    about,
    search,
)

urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='index'),
    path(
        'vacancies',
        VacancyListView.as_view(),
        name='vacancies'
    ),
    path(
        'vacancies/cat/<specialty>',
        VacancyBySpecialtyListView.as_view(),
        name='vacancy_by_specialty'
    ),
    path(
        'vacancies/<int:pk>',
        VacancyView.as_view(),
        name='vacancy_view'
    ),
    path(
        'vacancies/create',
        VacancyCreateView.as_view(),
        name='vacancy_create_view'
    ),
    path(
        'company/create',
        CompanyCreateView.as_view(),
        name='company_create_view'
    ),
    path(
        'companies/<int:pk>',
        CompanyView.as_view(),
        name='company_view'
    ),
    path(
        'mycompany',
        CompanyEditView.as_view(),
        name='my_company_view'
    ),
    path(
        'mycompany/vacancies',
        MyCompanyVacanciesView.as_view(),
        name='my_company_vacancies_view'
    ),
    path(
        'mycompany/vacancies/<int:pk>',
        MyCompanyVacancyView.as_view(),
        name='vacancy_view_from_account'
    ),
    path(
        'applications/<int:pk>',
        ApplicationsView.as_view(),
        name='applications_view'
    ),
    path(
        'about',
        about,
        name='about'
    ),
    path(
        # 'search?s=<query>',
        'search',
        search,
        name='search'
    ),

]
