from django.urls import path

from vacancies.views import (
    VacancyView,
    IndexView,
    VacancyListView,
    VacancyBySpecialtyListView,
    CompanyView,
    # my_company_view,
    MyCompanyVacanciesView,
    MyCompanyVacancyView,
    VacancySendView,
    CompanyCreateView,
    CompanyEditView, DataView
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
        'vacancies/<int:pk>',
        VacancyView.as_view(),
        name='vacancy_view'
    ),
    path(
        'vacancies/<int:pk>/send',
        DataView.as_view(),
        name='vacancy_send_view'
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
        name='my_company_vacancy_detail_view'
    ),

]
