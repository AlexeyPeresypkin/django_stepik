from django import forms
from django.forms import ModelForm

from vacancies.models import Company, Application, Vacancy


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'location',
            'logo',
            'description',
            'employee_count',
        ]


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = [
            'written_username',
            'written_phone',
            'written_cover_letter',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.vacancy = kwargs.pop('vacancy')
        super(ApplicationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ApplicationForm, self).save(commit=False)
        instance.vacancy = self.vacancy
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title',
            'specialty',
            'skills',
            'description',
            'salary_min',
            'salary_max',
        ]

