from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import *
from django.views import View
from registration.models import *
from django.db.models import *
from django.db.models.functions import  *
from registration.forms import StudentForm
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

# class CreateStudentView(View):
    # def get(self, request, *args, **kwargs):
    #     section_list = Section.objects.all()
    #     faculty_list = Faculty.objects.all()
    #     return render(request, "create_student.html", context={
    #             "total": section_list .count(),
    #             "faculty_list": faculty_list,
    #             "section_list": section_list
    #         })
    
    # def post(self, request, *args, **kwargs):
    #     # รับค่าจาก form
    #     student_id = request.POST.get("student_id")
    #     first_name = request.POST.get("first_name")
    #     last_name = request.POST.get("last_name")
    #     faculty_id = request.POST.get("faculty")
    #     email = request.POST.get("email")
    #     phone_number = request.POST.get("phone_number")
    #     address = request.POST.get("address")
    #     section_ids = request.POST.getlist("section_ids")

    #     # บันทึกลง database
    #     faculty = Faculty.objects.get(id=faculty_id)

    #     if section_ids != None:
    #         section = Section.objects.filter(id__in=section_ids)
    #         sd = Student.objects.create(
    #                 student_id=student_id,
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 faculty=faculty,
    #             )
    #         sd.enrolled_sections.set(section)
    #     else:
    #         sd = Student.objects.create(
    #                 student_id=student_id,
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 faculty=faculty,
    #             )
            
    #     StudentProfile.objects.create(
    #         student=sd,
    #         email=email,
    #         phone_number=phone_number,
    #         address=address,
    #     )


        
    #     return redirect("student_list")

def CreateStudentView(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(
                student_id = form.cleaned_data["student_id"],
                faculty = form.cleaned_data["faculty"],
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"]
            )
            student.enrolled_sections.set(form.cleaned_data["enrolled_sections"])
            StudentProfile.objects.create(
                student=student,
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
                address=form.cleaned_data["address"]
            )
            return redirect('student_list')
        print(form.errors)
        
    else:
        form = StudentForm()
    return render(request, "create_student.html", {"form": form})

def UpdateStudent(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    profile = getattr(student, 'studentprofile', None)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student.student_id = form.cleaned_data["student_id"]
            student.faculty = form.cleaned_data["faculty"]
            student.first_name = form.cleaned_data["first_name"]
            student.last_name = form.cleaned_data["last_name"]
            student.enrolled_sections.set(form.cleaned_data['enrolled_sections'])
            student.save()
            if profile:
                profile.email = form.cleaned_data['email']
                profile.phone_number = form.cleaned_data['phone_number']
                profile.address = form.cleaned_data['address']
                profile.save()
            else:
                StudentProfile.objects.create(
                    student = student,
                    email = form.cleaned_data['email'],
                    phone_number = form.cleaned_data['phone_number'],
                    address = form.cleaned_data['address']
                )
            return redirect("student_list")
        print(form.errors)
    else:
        initial_data = {
            'student_id' : student.student_id,
            'faculty' : student.faculty,
            "first_name": student.first_name,
            "last_name" : student.last_name,
            'enrolled_sections' : student.enrolled_sections.all(),
            'email' : profile.email,
            'phone_number' : profile.phone_number,
            'address' : profile.address
        }
        form = StudentForm(initial=initial_data)
    return render(request, "update_student.html", {"form": form})
