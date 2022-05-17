from django.contrib import admin

from vacancies.models import Company, Vacancy, Specialty, Application


@admin.register(Company, Vacancy, Specialty, Application)
class AuthorAdmin(admin.ModelAdmin):
    pass
