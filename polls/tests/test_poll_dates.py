import datetime
from .shortcut import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice


class QuestionTestCase(TestCase):
    """ Test cases for question model poll date"""

    def test_question_default_date(self):
        """ Check publish and end date default when create new question to be current date and time"""
        q = Question.objects.create(question_text="Test Question")
        time_ahead = timezone.now() + timezone.timedelta(milliseconds=10)
        time_behind = timezone.now() - timezone.timedelta(milliseconds=10)
        self.assertIs(time_behind <= q.pub_date <= time_ahead, True)

    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() returns False for questions
            whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently() returns False for question
            whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() returns True for questions
            whose pub_date is within last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_old_question(self):
        """
            is_published() return True for published question
        """
        old_question = create_question("Is Published old", pub_days=-1)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_default_question(self):
        """
            is_published() return True for published question that published at the moment
        """
        question = Question(question_text="Is Published old")
        self.assertIs(question.is_published(), True)

    def test_is_published_with_future_question(self):
        """
            is_published() return False for unpublished question
        """
        old_question = create_question("Is Published future", 1)
        self.assertIs(old_question.is_published(), False)

    def test_can_vote_with_unpublished_question(self):
        """
            can_vote() return False for question whose unpublished at the moment
        """
        question = create_question("Can vote unpublished", pub_days=1)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_future_end_date(self):
        """
            can_vote() return True for question whose published and end date is not reached
        """
        question = create_question("Can vote Future", -3, 1)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_with_past_end_date(self):
        """
            can_vote() return False for question whose published and end date is passed
        """
        question = create_question("Can vote past", -5, -2)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_no_end_date(self):
        """
            can_vote() return True for question whose published and end date is None
        """
        question = create_question("Can vote past", -5)
        self.assertIs(question.can_vote(), True)