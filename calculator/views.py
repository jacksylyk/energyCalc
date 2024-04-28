import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from calculator.forms import InvoiceForm
from calculator.models import Client, Contact, Invoice


# Create your views here.
@login_required
def index(request):
    return render(request, 'calculator/home.html')


def create_contacts_from_json(client_instance, json_data):
    contacts_array = json.loads(json_data)
    for contact_data in contacts_array:
        contact = Contact.objects.create(client=client_instance, contact=contact_data['phone'])


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    template_name = "calculator/create_client.html"
    success_url = "home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return self.save_with_contacts(form)

    def save_with_contacts(self, form):
        contacts_array = self.request.POST.get('contacts_array', None)
        if contacts_array:
            client_instance = form.save(commit=False)
            client_instance.save()
            create_contacts_from_json(client_instance, contacts_array)
        else:
            form.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.all()

    template_name = 'calculator/clients.html'


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'calculator/create_invoice.html'
    success_url = reverse_lazy('invoice_detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'calculator/invoice_detail.html'
    context_object_name = 'invoice'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Invoice, pk=pk)
