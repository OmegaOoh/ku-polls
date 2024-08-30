import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice


def create_question(question_text, pub_days, end_days = None):
    """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=pub_days)
    end_time = None
    if end_days != None:
        end_time = timezone.now() + datetime.timedelta(days=end_days)
    return Question.objects.create(question_text=question_text, pub_date=pub_time, end_date=end_time)


def create_choice(question, choice_text):
    """
        Create a choice for the given question with the given `question` with 'choices_text'
    """
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionTestCase(TestCase):
    """ Class to test the question model """

    def test_question_default_date(self):
        """ Check publish and end date default when create new question to be current date and time"""
        q = Question.objects.create(question_text="Test Question")
        time_ahead = timezone.now() + timezone.timedelta(milliseconds=10)
        time_behind = timezone.now() - timezone.timedelta(milliseconds=10)
        self.assertIs( time_behind <=q.pub_date <= time_ahead, True)

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
