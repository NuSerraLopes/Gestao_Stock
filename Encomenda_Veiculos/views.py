from django.shortcuts import render, redirect, get_object_or_404
from .models import OCFStock, Client, Vehicle, VP, Salesperson, ClientContact, InternalTransport
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'encomenda_veiculos/home.html')

# Client Views
class ClientListView(ListView):
    model = Client
    template_name = 'encomenda_veiculos/client_list.html'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'encomenda_veiculos/client_detail.html'

class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'encomenda_veiculos/client_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'encomenda_veiculos/client_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'encomenda_veiculos/client_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

# VP Views
class VPListView(ListView):
    model = VP
    template_name = 'encomenda_veiculos/vp_list.html'

class VPDetailView(DetailView):
    model = VP
    template_name = 'encomenda_veiculos/vp_detail.html'

class VPCreateView(CreateView):
    model = VP
    fields = '__all__'
    template_name = 'encomenda_veiculos/vp_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

class VPUpdateView(UpdateView):
    model = VP
    fields = '__all__'
    template_name = 'encomenda_veiculos/vp_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

class VPDeleteView(DeleteView):
    model = VP
    template_name = 'encomenda_veiculos/vp_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

# OCFStock Views
class OCFStockListView(ListView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_list.html'

class OCFStockDetailView(DetailView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_detail.html'

class OCFStockCreateView(CreateView):
    model = OCFStock
    fields = '__all__'
    template_name = 'encomenda_veiculos/ocfstock_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

class OCFStockUpdateView(UpdateView):
    model = OCFStock
    fields = '__all__'
    template_name = 'encomenda_veiculos/ocfstock_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

class OCFStockDeleteView(DeleteView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

# Salesperson Views
class SalespersonListView(ListView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_list.html'

class SalespersonDetailView(DetailView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_detail.html'

class SalespersonCreateView(CreateView):
    model = Salesperson
    fields = '__all__'
    template_name = 'encomenda_veiculos/salesperson_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

class SalespersonUpdateView(UpdateView):
    model = Salesperson
    fields = '__all__'
    template_name = 'encomenda_veiculos/salesperson_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

class SalespersonDeleteView(DeleteView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

# ClientContact Views
class ClientContactListView(ListView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_list.html'

class ClientContactDetailView(DetailView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_detail.html'

class ClientContactCreateView(CreateView):
    model = ClientContact
    fields = '__all__'
    template_name = 'encomenda_veiculos/clientcontact_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

class ClientContactUpdateView(UpdateView):
    model = ClientContact
    fields = '__all__'
    template_name = 'encomenda_veiculos/clientcontact_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

class ClientContactDeleteView(DeleteView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

# InternalTransport Views
class InternalTransportListView(ListView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_list.html'

class InternalTransportDetailView(DetailView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_detail.html'

class InternalTransportCreateView(CreateView):
    model = InternalTransport
    fields = '__all__'
    template_name = 'encomenda_veiculos/internaltransport_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')

class InternalTransportUpdateView(UpdateView):
    model = InternalTransport
    fields = '__all__'
    template_name = 'encomenda_veiculos/internaltransport_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')

class InternalTransportDeleteView(DeleteView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')
