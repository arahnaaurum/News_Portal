from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/personal.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/personal')