from django.forms import ModelForm

from vacancies.models import Company, Application


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
