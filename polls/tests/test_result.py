"""Test for Question Results Page."""

from .shortcut import create_question
from django.test import TestCase
from django.urls import reverse


class QuestionResultsViewTests(TestCase):
    """Module to test the result view of a question."""

    def test_future_result(self):
        """
        Result view of a question with future pub_date.

        User get redirected to index page.
        """
        future_question = create_question(question_text="Future question.",
                                          pub_days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_result(self):
        """
        Result view of question with pub_date set in the past.

        Result are shown for user correctly.
        """
        past_question = create_question(question_text="Past question.",
                                        pub_days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
