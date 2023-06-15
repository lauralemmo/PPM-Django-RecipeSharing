from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    CHOICES = [
        ('APPETIZER', 'Antipasto'),
        ('FIRST', 'Primo'),
        ('SECOND', 'Secondo'),
        ('SIDE', 'Contorno'),
        ('DESSERT', 'Dolce'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=100)
    persons = models.IntegerField(null=True)
    difficulty = models.IntegerField(null=True)
    category = models.CharField(max_length=10, choices=CHOICES, null=True)
    preparation_time = models.TimeField(null=True)
    ingredients = models.TextField(max_length=500, null=True)
    description = models.TextField(max_length=1000, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "recipes"


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorites"
