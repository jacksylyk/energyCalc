from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DeleteView, UpdateView, CreateView

from admin_panel.forms import OperatorCreationForm, OperatorChangeForm
from users.models import Operator


class SuperuserView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin.html')


class SuperuserUsersView(UserPassesTestMixin, ListView):
    model = Operator
    template_name = 'admin/manage_users.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class UserCreateView(UserPassesTestMixin, CreateView):
    model = Operator
    form_class = OperatorCreationForm
    template_name = 'admin/user_form.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = Operator
    form_class = OperatorChangeForm
    template_name = 'admin/user_form.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = Operator
    template_name = 'admin/user_confirm_delete.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class SuperuserClientsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/manage_clients.html')


class SuperuserInvoicesView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/manage_invoices.html')
