import django.test
from .shortcut import create_user, create_question, create_choice
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Choice
from django.conf import settings

class UserAuthTest(django.test.TestCase):

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        # Create a user with the correct username and password
        self.user1 = User.objects.create_user(username=self.username, password=self.password)
        
        # Create a question and choices for testing
        self.question = create_question("First Poll Question", 0)
        self.question.save()
        for n in range(1, 4):
            choice = create_choice(question=self.question, choice_text=f"Choice {n}")
            choice.save()

    def test_logout(self):
        """A user can logout using the logout url."""
        logout_url = reverse("logout")
        # Log in the user
        self.client.login(username=self.username, password=self.password)
        # Visit the logout page
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        # Can login using a POST request
        form_data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Authentication is required to submit a vote."""
        vote_url = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {"choice": f"{choice.id}"}
        # Attempt to vote without logging in
        response = self.client.post(vote_url, form_data)
        self.assertEqual(response.status_code, 302)
        login_with_next = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_with_next)