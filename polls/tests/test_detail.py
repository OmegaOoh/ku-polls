"""Module to test detail page of Polls app."""
from .shortcut import create_question, create_choice
from django.test import TestCase
from django.urls import reverse


class QuestionDetailViewTests(TestCase):
    """Module to test the detail view of a question."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date.

        Redirect user to index page(check for response code 302.
        """
        future_question = create_question(question_text="Future question.",
                                          pub_days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Published question detail page can be access by user."""
        past_question = create_question("Past question", -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoiceDetailViewTests(TestCase):
    """Module to test the choice of a question in detail view."""

    def test_one_choice(self):
        """Display a Choice that added to a question."""
        question = create_question(question_text="Past question", pub_days=-5)
        choice = create_choice(question, choice_text="Choice One")
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice.choice_text)

    def test_two_choices(self):
        """Display all available choices for a question."""
        question = create_question(question_text="Past question", pub_days=-5)
        choice1 = create_choice(question, choice_text="Choice One")
        choice2 = create_choice(question, choice_text="Choice Two")
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice1.choice_text, count=1)
        self.assertContains(response, choice2.choice_text, count=1)
