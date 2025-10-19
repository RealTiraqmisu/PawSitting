# from django.urls import path

# from . import views

# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"),
#     # ex: /polls/5/
#     path("<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

from django.urls import path
from . import views
urlpatterns = [
    path("student/", views.StudentView.as_view(), name="student_list"),
    path("professer/", views.ProfessorView.as_view(), name="professor_list"),
    path("course/", views.CourseView.as_view(), name="course_list"),
    path("faculty/", views.FacultyView.as_view(), name="faculty_list"),
    path("nav/", views.NavView.as_view(), name="nav"),
    path("create_student/", views.CreateStudentView, name="create_student"),
    # path("thanks/", views.thanks, name="thanks"),
    path("update/<str:student_id>/", views.UpdateStudent, name="update_student")
    ]