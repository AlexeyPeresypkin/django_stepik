from django.urls import path

from vacancies.views import VacancyView, IndexView, VacancyListView, \
    VacancyBySpecialtyListView, CompanyView

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
        'companies/<int:pk>',
        CompanyView.as_view(),
        name='company_view'
    ),
    path(
        'vacancies/<int:pk>',
        VacancyView.as_view(),
        name='vacancy_view'
    ),
]
