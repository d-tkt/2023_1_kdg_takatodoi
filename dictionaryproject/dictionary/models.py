from pyexpat import model
from django.db import models


CATEGORY = (('キャラクター', 'キャラクター'), ('企業・団体', '企業・団体'), ('種族', '種族'), ('その他', 'その他'))


class Dictionary(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)
    member = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY
    )

    def __str__(self):
        return self.title