from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

class UserProfile(models.Model):
    '''Модель профиля пользователя'''
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    user_photo=models.ImageField(
        upload_to='user_profiles'
    )

    def __str__(self):
        return self.user.username+' profile'



class Feedback(models.Model):
    '''Модель отзыва пользователя'''

    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
        )

    feedback_text=models.TextField(
        verbose_name='Оставьте отзыв',
        max_length=200
    )
    data_created=models.DateTimeField(
        verbose_name='Дата создание отзыва',
        default=timezone.now
    )

    def get_absolute_url(self):
        return reverse('feedback-details', kwargs={'pk':self.pk})


    def __str__(self):
        '''Описание объекта Feedback'''
        return f'{self.author.first_name}{self.author.last_name}'


class Comment(models.Model):

    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    feedback=models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='Текст отзыва',
        related_name='comments'
    )

    comment_text = models.CharField(
        verbose_name='Содержание отзыва',
        max_length=255
    )
    date_created = models.DateTimeField(
        verbose_name='Дата создания отзыва',
        default=timezone.now

    )
    def __str__(self):
        '''Описание объекта Comment'''
        return f'{self.author.first_name} {self.author.last_name} {self.date_created}'
