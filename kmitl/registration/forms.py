from django import forms
from .models import *
from django.forms import ModelForm
from registration.models import *
from django.core.exceptions import ValidationError

class StudentForm(ModelForm):
    # enrolled_sections = forms.ModelMultipleChoiceField(
    #     queryset=Section.objects.all(),
    #     required=False
    # )
    # email = forms.EmailField()
    # phone_number = forms.CharField(max_length=10)
    # address = forms.CharField(widget=forms.Textarea)
    # image = forms.FileField(
    #     required=False,
    #     widget=forms.ClearableFileInput(attrs={'class': 'hidden', 'id': 'image'})
    # )
    
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'faculty', 'enrolled_sections']
        


    # def save(self, commit=True):
    #     student_instance = super().save(commit=commit)
    #     profile, created = StudentProfile.objects.get_or_create(student=student_instance)

    #     profile.email = self.cleaned_data.get('email')
    #     profile.phone_number = self.cleaned_data.get('phone_number')
    #     profile.address = self.cleaned_data.get('address')
    #     image_data = self.cleaned_data.get('image')

    #     if image_data:
    #         profile.image = image_data

    #     profile.save()
    #     return student_instance

    
    def __str__(self):
        return f"{self.student_id} {self.first_name}"
    
class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['student']
        widgets = {
            "image":forms.ClearableFileInput(attrs={'class': 'hidden'})
        }
    def clean_email(self):
        data = self.cleaned_data['email']
        if data and not data.endswith("@kmitl.ac.th"):
            raise ValidationError("Email must end with kmitl.ac.th")
        return data
    
class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = '__all__'

class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ['course']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        
        if start_time >= end_time:
            self.add_error('end_time', "End time cannot be before start time")
        return cleaned_data
    
    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        if capacity <= 20:
            raise ValidationError("Capacity must greater than 20")
        return capacity
