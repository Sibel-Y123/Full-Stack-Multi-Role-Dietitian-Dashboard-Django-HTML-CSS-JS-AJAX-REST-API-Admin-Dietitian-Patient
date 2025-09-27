from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('dietitian', 'Dietitian'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class CustomerData(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    waist_cm = models.FloatField(null=True, blank=True)
    nutrition_score = models.FloatField(null=True, blank=True)

    def bmi(self):
        if self.height_cm > 0:
            return round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)
        return None

    def __str__(self):
        return f"{self.user.username} - {self.age} years"

