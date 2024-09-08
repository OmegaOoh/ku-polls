from  django.test import TestCase
from .shortcut import create_user, create_question, create_choice
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from django.conf import settings

class VoteCase(TestCase):
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

    def test_one_user_one_vote(self):
        vote_url = reverse('polls:vote', args=[self.question.id])
        self.client.force_login(self.user1)
        choice1 = self.question.choice_set.first()
        form_data = {"choice": f"{choice1.id}"}
        self.client.post(vote_url, form_data)  # First Vote
        self.assertEqual(choice1.votes, 1)

        choice2 = self.question.choice_set.last()
        form_data = {"choice": f"{choice2.id}"}
        self.client.post(vote_url, form_data)  # Update the vote
        self.assertEqual(choice2.votes, 1)
        
    def test_vote_updated(self):
        vote_url = reverse('polls:vote', args=[self.question.id])
        self.client.force_login(self.user1)
        choice1 = self.question.choice_set.first()
        form_data = {"choice": f"{choice1.id}"}
        choice1 = self.question.choice_set.first()
        self.client.post(vote_url, form_data)  # First Vote
        choice2 = self.question.choice_set.last()
        form_data = {"choice": f"{choice2.id}"}
        self.client.post(vote_url, form_data)  # Update the vote
        vote = choice2.vote_set.get(user=self.user1)
        self.assertEqual(vote.choice.id, choice2.id)