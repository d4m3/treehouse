from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms


class Dashboard(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    model = User
    select_related = ('thoughts',)
    template_name = 'users/dashboard.html'

    def get_object(self, queryset=None):
        return self.request.user


# Logout form layout
class LogoutView(LoginRequiredMixin, generic.FormView):
    form_class = forms.LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('home'))


# Sign up form layout
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:dashboard')


# # Company
# class CompanyCreate(LoginRequiredMixin, generic.CreateView):
#     form_class = forms.CompanyForm
#     success_url = reverse_lazy('users:dashboard')
#     template_name = 'users/form.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         response = super().form_valid(form)
#         self.object.members.add(self.request.user)
#         return response
























