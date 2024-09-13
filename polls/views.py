"""Module defined view class of each pages of Poll app."""

from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.signals import user_login_failed
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
user_choice = None  # Store choice in case of unauthenticated votes


class IndexView(generic.ListView):
    """Index view show all published questions."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now())\
            .order_by("-pub_date")


class DetailView(generic.DetailView):
    """Detail view show question detail, choices and vote button."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Override of get_context_data.

        Modify Context data.
        """
        context = super().get_context_data(**kwargs)
        # Check for previous selected choice
        if self.request.user.is_authenticated:
            try:
                # User is authenticated
                vote = Vote.objects.get(user=self.request.user,
                                        choice__question=self.question)
                context['voted_choice'] = vote.choice.id
            except (Vote.DoesNotExist):
                # User is not authenticated
                context['voted_choice'] = None
        return context

    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Override Get method.

        Check for question that does not exist and redirects user.
        """
        question_id = kwargs['pk']
        try:
            self.question = Question.objects.get(pk=question_id)
            if (not self.question.can_vote()):  # unpublished question/ closed.
                if (not self.question.is_published()):
                    raise Question.DoesNotExist("Unpublished Question")
                else:
                    return redirect(f"{reverse('polls:results', question_id)}")
            return super().get(request, *args, **kwargs)
        except (Question.DoesNotExist):
            return handle_access_non_exist_question(request, question_id)


class ResultsView(generic.DetailView):
    """Results view show question and each choice score."""

    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Override get context data method of Detail View."""
        context = super().get_context_data(**kwargs)
        try:
            if (self.request.user.is_authenticated):
                vote = Vote.objects.get(user=self.request.user,
                                        choice__question=self.question)
                context['voted_choice'] = vote.choice.id
            else:
                context['voted_choice'] = None
        except (Vote.DoesNotExist):
            context['voted_choice'] = None
        return context

    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        """Override of get method of an View superclass."""
        self.request = request
        question_id = kwargs['pk']
        try:
            self.question = Question.objects.get(pk=question_id)
            if not self.question.is_published():
                raise Question.DoesNotExist
            return super().get(request, *args, **kwargs)
        except (Question.DoesNotExist):
            return handle_access_non_exist_question(request, question_id)


def handle_access_non_exist_question(request, question_id):
    """Redirect user to index page when question is not exists."""
    messages.error(request, f"Polls {question_id} not exists.")
    error_str = f"IP {get_client_ip(request)} tried to access"\
                f"non-existent question (ID: {question_id})"
    logger.error(error_str)
    return redirect(f"{reverse('polls:index')}")


@login_required
def voting(request: HttpRequest, question_id: int) -> HttpResponse:
    """Handle votes POST request from vote button (detail page)."""
    global user_choice
    question = get_object_or_404(Question, pk=question_id)
    # Reference to current user
    cur_user = request.user
    try:
        if (user_choice is not None):
            selected_choice = user_choice
        else:
            selected_choice = question.choice_set\
                              .get(pk=request.POST["choice"])
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
        messages.success(request,
                         f"Your vote was updated to "
                         f"'{selected_choice.choice_text}'")
        log_str = f"User {cur_user.username} Update vote From {old_choice} "\
                  f"to {selected_choice.choice_text} "\
                  f"(Question: {question.question_text})"
        logger.info(log_str)
    except (KeyError, Vote.DoesNotExist):
        # User don't have a vote yet
        vote = Vote.objects.create(user=cur_user, choice=selected_choice)
        messages.success(request,
                         f"Your voted for '{selected_choice.choice_text}'")
        log_str = f"User {cur_user.username} "\
                  f"Vote choice{selected_choice.choice_text} "\
                  f"(Question: {question.question_text})"
        logger.info(log_str)
    selected_choice.save()
    # Redirect user to results page
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """Handle votes POST request from vote button (detail page)."""
    global user_choice
    if not request.user.is_authenticated:
        # User does not authenticated, save their choice before redirect
        question = get_object_or_404(Question, pk=question_id)
        try:
            user_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            user_choice = None
    response = voting(request, question_id)
    if request.user.is_authenticated:
        # user is now authenticated and those choice supposed to be processed
        # delete the user_choice after processed
        user_choice = None
    return response  # return the response from vote operation


# Logging for Authorization system
def get_client_ip(request):
    """Get IP address of visitor or user by HTTP request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get("REMOTE_ADDR")


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log user log in action."""
    ip_addr = get_client_ip(request)
    if (not user):
        logger.error(f"User is none in logged in request (IP: {ip_addr})")
    logger.info(f"User {user.username} has logged in (IP: {ip_addr})")


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log user log out action."""
    ip_addr = get_client_ip(request)
    if (not user):
        logger.error(f"User is none in logged out request (IP: {ip_addr})")
    logger.info(f"User {user.username} has logged out (IP: {ip_addr})")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Log user failed to login."""
    ip_addr = get_client_ip(request)
    username = credentials['username']
    logger.warn(f"User Failed Login to {username} (IP: {ip_addr})")
