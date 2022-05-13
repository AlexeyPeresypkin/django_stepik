from django.urls import path

from vacancies.views import index, vacancies, cat_view, companie_view, vacancie_view

urlpatterns = [
    path('', index, name='index'),
    path('vacancies', vacancies, name='vacancies'),
    path('vacancies/cat/frontend', cat_view, name='cat_view'),
    path('companies.json/345', companie_view, name='companie_view'),
    path('vacancies/22', vacancie_view, name='vacancie_view'),
]
