from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.messages import error, success

from polls.models import Question, Choice, Vote
from django.contrib import messages


class IndexView(generic.ListView):
    """
        Index view show all published questions.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions. """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
            Override Get method to check for question that does not exist and redirects user
        """
        try:
            Question.objects.get(pk=kwargs['pk'])
            return super().get(request, *args, **kwargs)
        except (Question.DoesNotExist):
            error(request, f"Polls {kwargs['pk']} not exists.")
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


@login_required
def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """ Handle votes POST request from vote button (detail page) """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        error(request, "You didn't select a choice.")
        context = {
            "question": question,
        }
        return render(request, 'polls/detail.html', context=context)
    if not question.can_vote():
        error(request, "This polls is closed.")
        context = {
            "question": question,
        }
        return render(request, 'polls/detail.html', context=context)
    # Reference to current user
    cur_user = request.user

    # Get the user vote's
    try:
        vote = cur_user.vote_set.get(choice__question=question)
        # user has a vote for this question, update the choice.
        vote.choice = selected_choice
        vote.save()
        messages.success(request,f"Your vote was updated to '{selected_choice.choice_text}'")
    except (KeyError, Vote.DoesNotExist):
        # user don't have a vote yet
        vote = Vote.objects.create(user=cur_user, choice=selected_choice)
        messages.success(request,f"Your voted for '{selected_choice.choice_text}'")
    selected_choice.save()
    # Redirect user to results page
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
