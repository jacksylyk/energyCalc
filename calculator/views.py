import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from calculator.models import Client, Contact, Invoice
from calculator.resources import ClientResource
import pandas as pd

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
    success_url = reverse_lazy('clients')

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
        queryset = Client.objects.all()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(bin_number__icontains=search_query) | Q(contract_number__icontains=search_query))
        return queryset

    template_name = 'calculator/clients.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'calculator/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('invoices')

class ClientExportView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        client_id = self.kwargs['client_id']
        client = Client.objects.get(pk=client_id)

        invoices = client.invoices.all()
        df = self.prepare_dataframe(invoices)

        # Export DataFrame to Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="client_invoices.xlsx"'
        df.to_excel(response, index=False)

        return response

    def prepare_dataframe(self, invoices):
        data = [
            {
                'Client': invoice.client,
                'Location': invoice.client.location,
                'Information': invoice.client.information,
                'Contract Date': invoice.client.contract_date,
                'Voltage': invoice.voltage,
                'BIN Number': invoice.client.bin_number,
                'Start': invoice.start,
                'End': invoice.end,
                'Consumption': invoice.consumption,
                'Without VAT': invoice.without_vat,
                'Meter Readings': [invoice.start, invoice.end]
            }
            for invoice in invoices
        ]

        df = pd.DataFrame(data)
        return df

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = '__all__'
    template_name = 'calculator/create_invoice.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.object:  # Check if self.object exists
            pk = self.object.pk
            return reverse_lazy('invoice_detail', kwargs={'pk': pk})
        else:
            # Provide a fallback URL if self.object is not defined
            return reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        client_id = self.request.GET.get('client_id')
        if client_id:
            kwargs['initial'] = {'client': client_id}
        return kwargs

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
