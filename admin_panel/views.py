from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DeleteView, UpdateView, CreateView
from django.views.generic.edit import FormView

from admin_panel.forms import OperatorCreationForm, OperatorChangeForm, OperatorPasswordResetForm
from calculator.models import Client, Invoice
from calculator.views import create_contacts_from_json
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


class UserResetPasswordView(UserPassesTestMixin, FormView):
    form_class = OperatorPasswordResetForm
    template_name = 'admin/reset_password_form.html'
    success_url = reverse_lazy('manage_users')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')

    def form_valid(self, form):
        user = Operator.objects.get(pk=self.kwargs['pk'])
        user.set_password(form.cleaned_data['new_password'])
        user.save()
        messages.success(self.request, "Пароль успешно сброшен.")
        return super().form_valid(form)


class SuperuserClientsView(UserPassesTestMixin, ListView):
    model = Client
    template_name = 'admin/manage_clients.html'
    context_object_name = 'clients'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = '__all__'
    template_name = "calculator/create_client.html"
    success_url = reverse_lazy('manage_clients')

    def test_func(self):
        # Replace with your own permission logic if needed
        return self.request.user.is_superuser or self.request.user == self.get_object().user

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')

    def form_valid(self, form):
        # Save client and contacts
        form.instance.user = self.request.user
        return self.save_with_contacts(form)

    def save_with_contacts(self, form):
        contacts_array = self.request.POST.get('contacts_array', None)
        client_instance = form.save(commit=False)
        client_instance.save()

        # Remove existing contacts
        client_instance.contacts.all().delete()

        # Add new contacts from JSON array
        if contacts_array:
            create_contacts_from_json(client_instance, contacts_array)

        return super().form_valid(form)


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'admin/client_confirm_delete.html'
    success_url = reverse_lazy('manage_clients')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['invoice_count'] = client.invoices.count()
        return context


class SuperuserInvoicesView(UserPassesTestMixin, ListView):
    model = Invoice
    template_name = 'admin/manage_invoices.html'
    context_object_name = 'invoices'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')


class InvoiceDeleteView(UserPassesTestMixin, DeleteView):
    model = Invoice
    template_name = 'admin/invoice_confirm_delete.html'
    success_url = reverse_lazy('manage_invoices')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "У вас недостаточно прав для доступа к этой странице.")
        return redirect('index')
