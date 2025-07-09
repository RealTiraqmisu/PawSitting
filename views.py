# polls/views.py
from django.http import HttpResponse

from django.shortcuts import render

from .models import Question

from datetime import datetime


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:1]
    context = {
        "page_title": "My first question",
        "question": latest_question_list,
        "current_date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
    return render(request, "index.html", context)

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {
        "question": question
    }
    return render(request, "detail.html", context)
    # return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)