"""Module to test the polls method in scope of dates and time."""

import datetime
from .shortcut import create_question
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionTestCase(TestCase):
    """Test cases for question model poll date."""

    def test_question_default_date(self):
        """Check for published with all default values."""
        q = Question.objects.create(question_text="Test Question")
        time_ahead = timezone.now() + timezone.timedelta(milliseconds=10)
        time_behind = timezone.now() - timezone.timedelta(milliseconds=10)
        self.assertIs(time_behind <= q.pub_date <= time_ahead, True)

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for unpublished question."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for old question.

        Return False as question is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for question published with a day."""
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_old_question(self):
        """is_published() return True for published question."""
        old_question = create_question("Is Published old", pub_days=-1)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False for unpublished question."""
        old_question = create_question("Is Published future", 1)
        self.assertIs(old_question.is_published(), False)

    def test_can_vote_with_unpublished_question(self):
        """can_vote() return False for question whose unpublished."""
        question = create_question("Can vote unpublished", pub_days=1)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_future_end_date(self):
        """can_vote() return True for end_date that not reached."""
        question = create_question("Can vote Future", -3, 1)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_with_past_end_date(self):
        """can_vote() return False for ended polls."""
        question = create_question("Can vote past", -5, -2)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_no_end_date(self):
        """can_vote() return True for question with no end date."""
        question = create_question("Can vote past", -5)
        self.assertIs(question.can_vote(), True)
