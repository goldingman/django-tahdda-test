from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=240)
    author = models.CharField(max_length=100)
    publishedDate = models.DateField()
    numberOfPages = models.IntegerField()

    def __str__(self) -> str:
        return self.title