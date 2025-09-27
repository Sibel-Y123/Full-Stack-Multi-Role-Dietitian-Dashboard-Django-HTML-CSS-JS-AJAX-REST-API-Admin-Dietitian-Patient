
from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    vitamin_c = models.FloatField(null=True, blank=True)
    iron = models.FloatField(null=True, blank=True)
    water = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    
