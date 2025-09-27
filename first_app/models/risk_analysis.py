
from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL kullanımı daha esnek olur

class RiskAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="risk_analysis")
    date = models.DateTimeField(auto_now_add=True)
    bmi = models.FloatField()
    risk_level = models.CharField(max_length=50)  # Low, Medium, High
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Risk Analysis - {self.user.username} ({self.date.date()})"
