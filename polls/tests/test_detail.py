import datetime
from .shortcut import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice


class QuestionDetailViewTests(TestCase):
    """
        Module to test the detail view of a question.
    """
    def test_future_question(self):
        """
            The detail view of a question with a pub_date in the future is return 404 not found.
        """
        future_question = create_question(question_text="Future question.", pub_days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
            The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question("Past question", -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoiceDetailViewTests(TestCase):
    """
        Module to test the choice of a question in detail view.
    """
    def test_one_choice(self):
        """ Display a Choice that added to a question"""
        question = create_question(question_text="Past question", pub_days=-5)
        choice = create_choice(question, choice_text="Choice One")
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice.choice_text)

    def test_two_choices(self):
        """ Display all available choices for a question """
        question = create_question(question_text="Past question", pub_days=-5)
        choice1 = create_choice(question, choice_text="Choice One")
        choice2 = create_choice(question, choice_text="Choice Two")
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice1.choice_text, count=1)
        self.assertContains(response, choice2.choice_text, count=1)
