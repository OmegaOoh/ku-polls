"""Module contains Class of Model of each entity stored in database."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model to store the question text and its publication date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',
                                    default=timezone.now)
    end_date = models.DateTimeField('poll end date',
                                    blank=True, null=True,
                                    default=None)

    def __str__(self):
        """Return question text as a string representative of Question."""
        return self.question_text

    def was_published_recently(self):
        """
        Check if whether the question has been published recently.

        :return: True if this question has been published within 24 hours,
        else False
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Check if the question is in the published period.

        :return: Boolean, True if current date is on or after publication date
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """
        Check if the voting is allow on the question.

        :return: returns True if voting is allowed for this question.
          That means,the current date/time is between the pub_date and end_date
        """
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        return self.is_published() and now < self.end_date


class Choice(models.Model):
    """
    Choices model to store choices of the question with its votes.

    Has Question(class) as a ForeignKey
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Return the votes for this choice."""
        return self.vote_set.count()

    def __str__(self):
        """Return choice_text as string representative."""
        return self.choice_text


class Vote(models.Model):
    """Vote model to store votes of the choices by a user."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
