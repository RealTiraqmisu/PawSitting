from django import forms
from .models import *
from django.forms import ModelForm
from registration.models import *
from django.core.exceptions import ValidationError

# class StudentForm(forms.Form):
#     student_id = forms.CharField(max_length=10)
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     faculty = forms.ModelChoiceField(
#         queryset=Faculty.objects.all(),
#         empty_label="Select an option",
#         required=False,
#         widget=forms.RadioSelect
#     )
#     enrolled_sections = forms.ModelMultipleChoiceField(
#         queryset=Section.objects.all(),
#         required=False,
#     )
#     email = forms.EmailField()
#     phone_number = forms.CharField(max_length=10)
#     address = forms.CharField(widget=forms.Textarea)
#     def __str__(self):
#         return f"{self.student_id} - {self.first_name}"

class StudentForm(ModelForm):
    enrolled_sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(),
        required=False
    )
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'faculty', 'enrolled_sections']

    def clean_email(self):
        data = self.cleaned_data['email']
        if data and not data.endswith("@kmitl.ac.th"):
            raise ValidationError("Email must end with kmitl.ac.th")
    def __str__(self):
        return f"{self.student_id} - {self.first_name}"
    
class CourseForm(ModelForm):
    section_number = forms.CharField(max_length=3)
    semester = forms.CharField(max_length=10)
    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        required=False
    )
    day_of_week = forms.ChoiceField(choices=Section.DayOfWeek.choices)
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), input_formats=['%H:%M'])
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), input_formats=['%H:%M'])
    capacity = forms.IntegerField(default=60)
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credits']

# course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     section_number = models.CharField(max_length=3)
#     semester = models.CharField(max_length=10)
#     professor = models.ForeignKey(
#         Professor, on_delete=models.SET_NULL, null=True, blank=True
#     )
#     day_of_week = models.CharField(max_length=3, choices=DayOfWeek.choices)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     capacity = models.PositiveSmallIntegerField(default=60)