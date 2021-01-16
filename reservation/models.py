from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

class Order(models.Model):
    '''Модель бронирование.
    Имеет 7 полей для создание брони'''

    reservator=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )


    phone=models.IntegerField(
        verbose_name='Номер телефона'
    )


    date=models.DateField(
        verbose_name='Дата бронирование'
    )


    time=models.TimeField(
        verbose_name='Время бронирование'
    )


    PERSONS=(
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6)
    )





    persons=models.CharField(
        verbose_name='Количество человек',
        choices=PERSONS,
        default=PERSONS[0][1],
        max_length=1
    )

    message=models.TextField(
        verbose_name='Комментарии',
        max_length=500,
        blank=True,
        default='Комментариев нет'
    )

    date_created=models.DateTimeField(
        verbose_name='Дата создание заказа',
        default=timezone.now
    )

    def get_absolute_url(self):
        return reverse('reservation:my_reservation')

    def __str__(self):
        '''Описание обьекта Order'''
        return f'{self.reservator} {self.date} {self.time}'





