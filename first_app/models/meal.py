from django.db import models
from django.conf import settings
from .food import Food

class MealLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_logs')
    date = models.DateField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text='in terms of gram')

    def total_calories(self):
        return round(self.food.calories * self.quantity / 100, 2)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} ({self.date})"

