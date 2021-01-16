from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Cook(models.Model):
    '''Модель сoтрудников'''

    POSITION=(
        ('Гениральный директор', 'Гениральный директор'),
        ('Шеф повар', 'Шеф повар'),
        ('Повар', 'Повар'),
        ('Стажер', 'Стажер'),
    )

    EDUCATION=(
        ('Бакалавр', 'Бакалавр'),
        ('Техникум или Коледж', 'Техникум или Коледж'),
        ('Самоучка', 'Самоучка')
    )


    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )


    position=models.CharField(
        verbose_name='Должность',
        choices=POSITION,
        default=POSITION[0][1],
        max_length=100
    )


    education=models.CharField(
        verbose_name='Образование',
        choices=EDUCATION,
        default=EDUCATION[0][1],
        max_length=100
    )

    experience=models.IntegerField(
        verbose_name='Реальный стаж работы'
    )

    work_history=models.CharField(
        verbose_name='История Работы',
        max_length=250
    )

    def get_absolute_url(self):
        return reverse('teams:teams')


    def __str__(self):
        return f'{self.user} {self.pk} {self.position}'


