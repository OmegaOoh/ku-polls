import datetime
from .shortcut import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice


class QuestionIndexViewTests(TestCase):
    """
        Module to test the index view on question.
    """
    def test_no_question(self):
        """
            If no question exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
            If question is published in the past, displayed the question correctly
        """
        question = create_question(question_text="Past question.", pub_days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """
            Questions with a pub_date in the future aren't displayed on the index page.
        """
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
            Even if both Future and past question exist, only past question is displayed.
        """
        create_question("Future question", 30)
        question = create_question("Past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        """
            The question index page may display multiple questions.
        """
        question1 = create_question("Past Question 1", -30)
        question2 = create_question("Past Question 2", -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])
