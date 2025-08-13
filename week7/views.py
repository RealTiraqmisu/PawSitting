from django.shortcuts import render

from django.views import View
from registration.models import *
from django.db.models import *
from django.db.models.functions import *

# Create your views here.
class StudentView(View):
    def get(self, request):
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")

        filters = {}
        if filter_type == "":
            filters["full_name__icontains"] = search_txt
        elif filter_type == "email":
            filters["studentprofile__email__icontains"] = search_txt
        elif filter_type == "faculty":
            filters["faculty__name__icontains"] = search_txt

        student_list = Student.objects.annotate(
            full_name = Concat("first_name", Value(" "), "last_name")
        ).filter(**filters)

        return render(request, "index.html", context={
            "total": student_list.count(),
            "student_list": student_list,
            "filter": filter_type,
            "search": search_txt
        })
class ProfessorView(View):
    def get(self, request):
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")

        filters = {}
        if filter_type == "":
            filters["full_name__icontains"] = search_txt
        elif filter_type == "faculty":
            filters["faculty__name__icontains"] = search_txt

        professor_list = Professor.objects.annotate(
            full_name = Concat("first_name", Value(" "), "last_name")
        ).filter(**filters)

        return render(request, "professor.html", context={
            "total": professor_list.count(),
            "professor_list": professor_list,
            "filter": filter_type,
            "search": search_txt
        })
class CourseView(View):
    def get(self, request):
        search_txt = request.GET.get("search")

        if search_txt != None:
            filters = {}
            filters["course_name__icontains"] = search_txt
            course_list = Course.objects.all().filter(**filters)
        else:
            course_list = Course.objects.all()
        
        return render(request, "course.html", context={
            "total": course_list.count(),
            "course_list": course_list,
            "search": search_txt
        })
    
class FacultyView(View):
    def get(self, request):

        search_txt = request.GET.get("search")
        # filter_type = request.GET.get("filter")
        if search_txt != None:
            filters = {}
            filters["name__icontains"] = search_txt

            faculty_list = Faculty.objects.annotate(
                prof = Count("professor", distinct=True),
                stud = Count("student", distinct=True)
            ).filter(**filters)
        else:
            faculty_list = Faculty.objects.annotate(
                prof = Count("professor", distinct=True),
                stud = Count("student", distinct=True)
            )

        return render(request, "faculty.html", context={
            "total": faculty_list.count(),
            "faculty_list": faculty_list,
            # "filter": filter_type,
            "search": search_txt
        })
