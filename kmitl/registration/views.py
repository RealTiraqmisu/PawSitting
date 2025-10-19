from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import *
from django.views import View
from registration.models import *
from django.db.models import *
from django.db.models.functions import  *
from registration.forms import *
from django.db import transaction

# Create your views here.
class StudentView(View):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

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
            full_name=Concat("first_name", Value(" "), "last_name")
        ).filter(**filters)
        
        return render(request, "index.html", context={
            "total": student_list.count(),
            "student_list": student_list,
            "filter": filter_type,
            "search":search_txt
        })
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

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
            full_name=Concat("first_name", Value(" "), "last_name")
        ).filter(**filters)
        return render(request, "professor.html", context={
            "total": professor_list.count(),
            "professor_list": professor_list,
            "filter": filter_type,
            "search":search_txt
            
        })
    
class CourseView(View):

    def get(self, request):
        search_txt = request.GET.get("search") or ""


        filters = {}
        filters["course_name__icontains"] = search_txt
        course_list = Course.objects.all().filter(**filters)
        return render(request, "course.html", context={
                "total": course_list.count(),
                "course_list": course_list,
                "search":search_txt
            })
    
class FacultyView(View):
    

    def get(self, request):
        search_txt = request.GET.get("search")  or ""

        filters = {}
        filters["name__icontains"] = search_txt
        faculty_list = Faculty.objects.annotate(cst=Count("student", distinct=True), cpro=Count("professor", distinct=True)).filter(**filters)
        return render(request, "faculty.html", context={
                "total": faculty_list.count(),
                "faculty_list": faculty_list,
                "search":search_txt
            })

class NavView(View):
    def index(request):
        return render(request ,"nav.html")

def CreateStudentView(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        form2 = StudentProfileForm(request.POST, request.FILES)
        try:
            with transaction.atomic():
                if form.is_valid():
                    student = form.save()
                    if form2.is_valid():
                        profile = form2.save(commit=False)
                        profile.student = student
                        profile.save()
                        return redirect('student_list')
                    raise transaction.TransactionManagementError("Student Profile form invalid")
                raise transaction.TransactionManagementError("Student form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "create_student.html", {"form": form, 'form2': form2})
    else:
        form = StudentForm()
        form2 = StudentProfileForm()
    return render(request, "create_student.html", {"form": form, 'form2': form2})

def CreateCourseView(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, "create_course.html", {"form": form})
    
def UpdateStudent(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    profile = getattr(student, 'studentprofile', None)
    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        form2 = StudentProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid() and form2.is_valid():
            student = form.save()
            profile = form2.save(commit=False)
            profile.student = student
            profile.save()
            student.enrolled_sections.set(form.cleaned_data['enrolled_sections'])
            return redirect("student_list")
        # print(form.errors)
    else:
        form = StudentForm(instance=student)
        form2 = StudentProfileForm(instance=profile)
    return render(request, "update_student.html", {"form": form, "form2": form2, 'student': student})

class UpdateCourse(View):
    def get(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)
        section = Section.objects.filter(course=course).first()
        print(section)
        form1 = CourseForm(instance=course)
        form2 = SectionForm(instance=section)
        context = {
            'form1': form1,
            'form2': form2
        }
        return render(request, 'update_course.html', context)
    
    def post(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)
        section = Section.objects.filter(course=course).first()
        form1 = CourseForm(request.POST, instance=course)
        form2 = SectionForm(request.POST, instance=section)

        if form1.is_valid() and form2.is_valid():
            f1 = form1.save()
            f2 = form2.save(commit=False)
            f2.course = f1
            f2.save()
            print("pass")
            return redirect('course_list')
        context = {
            'form1': form1,
            'form2': form2
        }
        return render(request, 'update_course.html', context)
