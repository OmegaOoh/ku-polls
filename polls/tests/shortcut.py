"""Module contains shortcut function to use in testcases."""

import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from polls.models import Question, Choice


def create_question(question_text, pub_days, end_days=None):
    """
    Create a question with given argument.

    :return: question object with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=pub_days)
    end_time = None
    if end_days is not None:
        end_time = timezone.now() + datetime.timedelta(days=end_days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=pub_time,
                                   end_date=end_time)


def create_choice(question, choice_text):
    """
    Create a choice from given argument.

    :return: choice object with given question and choice_text.
    """
    return Choice.objects.create(question=question, choice_text=choice_text)


def create_user(username, password):
    """Create a user with specifics username and password."""
    return User.objects.create_user(username=username, password=password)
