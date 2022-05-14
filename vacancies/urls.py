from django.urls import path

from vacancies.views import cat_view, companie_view, \
    vacancie_view, IndexView, VacancyListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('vacancies', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/cat/frontend', cat_view, name='cat_view'),
    path('companies.json/345', companie_view, name='companie_view'),
    path('vacancies/22', vacancie_view, name='vacancie_view'),
]
