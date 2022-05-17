from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from vacancies.models import Company


class RecipeForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name',
                  'location',
                  'logo',
                  'description',
                  'employee_count',
                  ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }