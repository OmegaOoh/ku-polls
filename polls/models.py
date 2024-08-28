import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """ Question model to store the question text and its publication date"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('poll end date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Check if whether the question has been published recently.
        :return: True if this question has been published within 24 hours, else False
        """
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
