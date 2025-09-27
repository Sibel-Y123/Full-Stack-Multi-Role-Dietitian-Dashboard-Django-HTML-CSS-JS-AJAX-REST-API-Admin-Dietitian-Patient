# first_app/forms.py
from first_app.models import CustomerData, User
from django import forms

class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = CustomerData
        fields = ['user', 'age', 'gender', 'height_cm', 'weight_kg', 'waist_cm', 'nutrition_score']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'nutrition_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your current password"})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your new password"})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm  your new password"})
    )





