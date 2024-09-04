""" Module contains shortcut function to use in testcases """

import datetime
from django.utils import timezone
from polls.models import Question, Choice

def create_question(question_text, pub_days, end_days=None):
    """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=pub_days)
    end_time = None
    if end_days is not None:
        end_time = timezone.now() + datetime.timedelta(days=end_days)
    return Question.objects.create(question_text=question_text, pub_date=pub_time, end_date=end_time)


def create_choice(question, choice_text):
    """
        Create a choice for the given question with the given `question` with 'choices_text'
    """
    return Choice.objects.create(question=question, choice_text=choice_text)

