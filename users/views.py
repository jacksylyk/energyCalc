from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # Add other profile data as needed
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/edit.html'
    fields = "first_name", "last_name", "second_name"
    success_url = reverse_lazy('users:me')  # Redirects to profile page after successful update

    def get_object(self, queryset=None):
        return self.request.user
