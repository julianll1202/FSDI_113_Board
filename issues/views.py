from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Issue, Status

from accounts.models import Role, Team, CustomUser


class BoardView(LoginRequiredMixin, ListView):
    template_name = "issues/board.html"
    model = Issue
    
    def populate_issue_list(self, name, status, reporter, context):
        context[name] = Issue.objects.filter(
            status=status
        ).filter(
            reporter=reporter
        ).order_by(
            "created_on"
        ).reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do_status = Status.objects.get(id=1)
        in_p_status = Status.objects.get(id=2)
        done_status = Status.objects.get(id=3)

        team = self.request.user.team
        role = Role.objects.get(name="Product owner")

        
        
        try:
            product_owner = CustomUser.objects.filter(
            role=role).filter(team=team)[0]
            self.populate_issue_list("to_do_list", to_do_status, product_owner, context)
            self.populate_issue_list("in_p_list", in_p_status, product_owner, context)
            self.populate_issue_list("done_list", done_status, product_owner, context)
        except Exception:
            context["to_do_list"] = []
            context["in_p_list"] = []
            context["done_list"] = []
        return context

class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "status", "priority", "assignee"]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "issues/update.html"
    model = Issue
    fields = ["summary", "description", "status", "priority", "assignee"]

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy('board')

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user