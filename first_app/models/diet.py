from django.db import models
from django.conf import settings

class DietPlan(models.Model):
    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='plans_created', 
        limit_choices_to={'role': 'dietitian'}
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        
        on_delete=models.CASCADE, 
        related_name='plans_received', 
        limit_choices_to={'role': 'patient'}
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Plan: {self.dietitian.username} → {self.patient.username}"

