from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import available_attrs, method_decorator
from django.utils.translation import gettext_lazy as _

from vote.models import *
from majority_judgment.tools import *

# Create your views here.



@login_required
def redirect_candidates(request):
    try:
        voter       = Voter.objects.filter(user=request.user).first()
        election_id = voter.election.pk
        return HttpResponseRedirect('/candidates/{:d}/'.format(election_id))
    except Voter.DoesNotExist:
        return render(request, 'vote/error.html', {"message":_("No election has been found for you...")})


class CandidateList(LoginRequiredMixin, generic.ListView):
    model = Candidate
    template_name = "candidate/candidate_list.html"

    def get_queryset(self):
        try:
            self.election = Election.objects.get(pk=self.kwargs['election_id'])
            self.voter = Voter.objects.filter(election=self.election,
                                              user=self.request.user)
        except Election.DoesNotExist:
            return render(request, 'vote/error.html', {"message":_("The election does not exist")})
        except Voter.DoesNotExist:
            return render(request, 'vote/error.html', {"message":_("You are not allowed to be here")})
        return Candidate.objects.filter(election=self.election)

    def get_context_data(self, **kwargs):
        context = super(CandidateList, self).get_context_data(**kwargs)
        context['election'] = self.election
        context['voter'] = self.voter
        return context


class CandidateDetail(LoginRequiredMixin, generic.DetailView):
    model = Candidate

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)
        context['election'] = self.election
        return context
