from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Vacancy(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    specialty = models.ForeignKey(
        max_length=128,
        verbose_name='Специализация',
        related_name='vacancies',
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        max_length=128,
        verbose_name='Компания',
        related_name='vacancies',
        on_delete=models.CASCADE
    )
    skills = models.CharField(
        max_length=255,
        verbose_name='Навыки'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    salary_min = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Зарплата от'
    )
    salary_max = models.IntegerField(
        validators=[MinValueValidator(2)],
        verbose_name='Зарплата до'
    )
    published_at = models.DateField(
        auto_now_add=True,
        verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancies:vacancy', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Company(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    location = models.CharField(
        max_length=255,
        verbose_name='Город'
    )
    logo = models.CharField(
        max_length=255,
        verbose_name='Логотипчик',
        blank=True
    )
    description = models.TextField(
        verbose_name='Информация о компании',
        blank=True
    )
    employee_count = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество сотрудников',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vacancies:company', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(models.Model):
    code = models.CharField(
        max_length=255,
        verbose_name='Код'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    picture = models.CharField(
        max_length=255,
        verbose_name='Картинка',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancies:specialty', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
