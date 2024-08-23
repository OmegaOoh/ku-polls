import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """ Question model to store the question text and its publication date"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    datetime.timedelta(days=1)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """ Choices model to store choices of the question with its current number of votes
        Has Question(class) as a ForeignKey
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
