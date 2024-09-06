import datetime

from .shortcut import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice

class QuestionResultsViewTests(TestCase):
    """
        Module to test the result view of a question.
    """
    def test_future_result(self):
        """
            The result view of a question with a pub_date in the future is return 404 not found.
        """
        future_question = create_question(question_text="Future question.", pub_days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_result(self):
        """
            The result view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text="Past question.", pub_days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
