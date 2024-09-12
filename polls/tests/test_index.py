"""Module to test index page of polls app."""

from .shortcut import create_question
from django.test import TestCase
from django.urls import reverse


class QuestionIndexViewTests(TestCase):
    """Module to test the index view on question."""

    def test_no_question(self):
        """If no question exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Published question showed on index page."""
        question = create_question(question_text="Past question.",
                                   pub_days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'],
                                 [question])

    def test_future_question(self):
        """Unpublished question does not show on index page."""
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        Only published question is show on index page.

        Unpublished polls does not show up on index page.
        """
        create_question("Future question", 30)
        question = create_question("Past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'],
                                 [question])

    def test_two_past_question(self):
        """The question index page may display multiple questions."""
        question1 = create_question("Past Question 1", -30)
        question2 = create_question("Past Question 2", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'],
                                 [question2, question1])
