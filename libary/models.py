from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=100)
    auther=models.CharField(max_length=150)
    published_date=models.DateField()
    price=models.DecimalField(max_digits=6,decimal_places=2)

def __str__(self):
    return self.title