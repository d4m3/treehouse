from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy,reverse
from django.views import generic


# Used for Update
from braces.views import SetHeadlineMixin

from ..import models
from .. import forms
from ..models import Family


# Create
class Create(LoginRequiredMixin, SetHeadlineMixin, generic.CreateView):
    form_class = forms.FamilyForm
    headline = 'Create Family'
    success_url = reverse_lazy('users:dashboard')
    template_name = 'families/form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response


# Update
class Update(LoginRequiredMixin, SetHeadlineMixin, generic.UpdateView):
    form_class = forms.FamilyForm
    # success_url = reverse_lazy('users:dashboard')
    template_name = 'families/form.html'

    def get_queryset(self):
        return self.request.user.families.all()

    def get_headline(self):
        return f'Edit {self.object.name}'

    # Send user to this page after successfully updating
    def get_success_url(self):
        return reverse('groups:families:detail', kwargs={'slug':self.object.slug})


# View Details
class Detail(LoginRequiredMixin, generic.DetailView):
    template_name = 'families/detail.html'

    def get_queryset(self):
        return self.request.user.families.all()


# Leave Family
class Leave(LoginRequiredMixin, SetHeadlineMixin, generic.FormView):
    form_class = forms.LeaveForm
    template_name = 'families/form.html'
    success_url = reverse_lazy('users:dashboard')

    def get_object(self):
        try:
            self.object = self.request.user.families.filter(
            slug=self.kwargs.get('slug'),
            ).exclude(created_by=self.request.user).get()
        except models.Family.DoesNotExist:
            raise Http404()

    def get_headline(self):
        self.get_object()
        return f'Leave {self.object}?'

    def form_valid(self, form):
        self.get_object()
        self.object.members.remove(self.request.user)
        return super().form_valid(form)



# View for seeing an invitation to a group
class Invites(LoginRequiredMixin, generic.ListView):
    template_name = 'families/invites.html'

    def get_queryset(self):
        return self.request.user.familyinvite_received.filter(status=0)



# View to accept/reject invitation
# Accept go back to invites page
# Reject 404
class InviteResponse(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('groups:families:invites')

    def get(self, request, *args, **kwargs):
        invite = get_object_or_404(
            models.FamilyInvite,
            to_user=request.user,
            uuid=kwargs.get('code'),
            status=0
        )
        if kwargs.get('response') == 'accept':
            invite.status = 1
        else:
            invite.status = 2

        invite.save()

        return super().get(request, *args, **kwargs)










































































