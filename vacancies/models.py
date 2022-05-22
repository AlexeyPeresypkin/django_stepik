from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from src.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR

User = get_user_model()


class Company(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    location = models.CharField(
        max_length=255,
        verbose_name='Город'
    )
    logo = models.ImageField(
        upload_to=MEDIA_COMPANY_IMAGE_DIR,
        verbose_name='Логотипчик',
    )
    description = models.TextField(
        verbose_name='Информация о компании',
    )
    employee_count = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество сотрудников',
    )
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='company',
        blank=True,
        null=True,
        default=None
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
    picture = models.ImageField(
        upload_to=MEDIA_SPECIALITY_IMAGE_DIR,
        verbose_name='Картинка',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancies:specialty', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Vacancy(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    specialty = models.ForeignKey(
        Specialty,
        max_length=128,
        verbose_name='Специализация',
        related_name='vacancies',
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
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


class Application(models.Model):
    written_username = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    written_phone = models.CharField(
        max_length=128,
        verbose_name='Телефон'
    )
    written_cover_letter = models.TextField(
        verbose_name='Сопроводительное письмо'
    )
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='applications',
        on_delete=models.CASCADE,
        verbose_name='Вакансия'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.written_username

    # def get_absolute_url(self):
    #     return reverse('vacancies:vacancy', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
