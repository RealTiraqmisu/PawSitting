from django import forms
from pawsitting.models import *
from django.forms import ModelForm
from pawsitting.models import *
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta, date
from django.contrib.auth import get_user_model

def cal_total(service, start, end):
    day = (end-start).days + 1
    return service.price * day

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'start_date', 'end_date']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date >= end_date:
            self.add_error('end_date', "End date must be at least 1 day from start date.")
            return cleaned_data
        
        if start_date < (date.today() + timedelta(days=1)):
            self.add_error('start_date', "Start date must be at least 1 day from today.")
            return cleaned_data

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'})
        }

class SitterRegistrationForm(ModelForm):
    class Meta:
        model = SitterProfile
        fields = ['bio', 'service', 'cert_image']
        widgets = {
            "bio": forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            "cert_image": forms.FileInput(attrs={'class': 'hidden'})
        }

class VerifySitterForm(ModelForm):
    class Meta:
        model = SitterProfile
        fields = ['is_verified']
        widgets = {
            "is_verified": forms.CheckboxInput(attrs={'class': 'form-control'})
        }

class StatusForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

class RatingForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating']
        widgets = {
            'rating': forms.Select(
                choices=[
                    (5, 'ดีเยี่ยม'),
                    (4, 'ดี'),
                    (3, 'พอใช้'),
                    (2, 'แย่'),
                    (1, 'แย่มาก')
                ],
                attrs={'class': 'form-control'})
        }

class EditUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']