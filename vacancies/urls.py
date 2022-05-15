from django.urls import path

from vacancies.views import companie_view, \
    vacancie_view, IndexView, VacancyListView, VacancyBySpecialtyListView

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
        'companies.json/345',
        companie_view,
        name='companie_view'
    ),
    path(
        'vacancies/22',
        vacancie_view,
        name='vacancie_view'
    ),
]
