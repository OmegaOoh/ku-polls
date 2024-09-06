from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import django.contrib.messages as messages
from django.dispatch import receiver
import logging

from polls.models import Question, Choice, Vote

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    """
        Index view show all published questions.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions. """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    """
        Detail view show question detail including the choice and vote button.
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
            Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """ Override of get_context_data method to add/modify the context data"""
        context = super().get_context_data(**kwargs)
        # Check for previous selected choice
        if self.request.user.is_authenticated:
            try:
                # User is authenicated
                vote = Vote.objects.get(user=self.request.user, choice__question=self.question)
                context['voted_choice'] = vote.choice.id
            except (Vote.DoesNotExist):
                # User is not authenicated
                context['voted_choice'] = None
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
            Override Get method to check for question that does not exist and redirects user
        """
        question_id = kwargs['pk']
        try:
            self.question = Question.objects.get(pk=question_id)
            return super().get(request, *args, **kwargs)
        except (Question.DoesNotExist):
            messages.error(request, f"Polls {question_id} not exists.")
            logger.error(f"IP {get_client_ip(request)} tried to access non-existent question (ID: {question_id})")
            return redirect(f"{reverse('polls:index')}")


class ResultsView(generic.DetailView):
    """
        Results view show question and each choice score.
    """
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """
            Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if (self.request.user.is_authenticated):
            vote = Vote.objects.get(user=self.request.user, choice__question=self.question)
            context['voted_choice'] = vote.choice.id
        else:
            context['voted_choice'] = None
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        question_id = kwargs['pk']
        self.question = Question.objects.get(pk=question_id)
        return super().get(request, *args, **kwargs)


@login_required
def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """ Handle votes POST request from vote button (detail page) """
    question = get_object_or_404(Question, pk=question_id)
    # Reference to current user
    cur_user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        messages.error(request, "You didn't select a choice.")
        context = {
            "question": question,
        }
        return render(request, 'polls/detail.html', context=context)
    if not question.can_vote():
        messages.error(request, "This polls is closed.")
        context = {
            "question": question,
        }
        return render(request, 'polls/detail.html', context=context)

    # Get the user vote's
    try:
        vote = cur_user.vote_set.get(choice__question=question)
        old_choice = vote.choice.choice_text
        # User has a vote for this question, update the choice.
        vote.choice = selected_choice
        vote.save()
        messages.success(request, f"Your vote was updated to '{selected_choice.choice_text}'")
        logger.info(f"User {cur_user.username} Update vote From {old_choice} to {selected_choice.choice_text} (Question: {question.question_text})") 
    except (KeyError, Vote.DoesNotExist):
        # User don't have a vote yet
        vote = Vote.objects.create(user=cur_user, choice=selected_choice)
        messages.success(request, f"Your voted for '{selected_choice.choice_text}'")
        logger.info(f"User {cur_user.username} Vote choice{selected_choice.choice_text} (Question: {question.question_text})")
    selected_choice.save()
    # Redirect user to results page
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# Logging for Authorization system
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get("REMOTE_ADDR")


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"User {user.username} has logged in (IP: {ip_addr})")


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"User {user.username} has logged out (IP: {ip_addr})")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip_addr = get_client_ip(request)
    username = credentials['username']
    logger.warn(f"User Failed Login to {username} (IP: {ip_addr})")
