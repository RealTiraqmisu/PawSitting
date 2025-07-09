from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=150)
    description = models.TextField(null=True)
    pub_date = models.DateTimeField("date published", auto_now=False)
    # object.<class_fk>_set.all()
    # object.choice_set.all()
    # object.description_set.all()
    # Quetsion.objects.filter()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)