from django.shortcuts import render, redirect, get_object_or_404
from .models import OCFStock, Client, Vehicle, VP, Salesperson, ClientContact, InternalTransport
from .forms import OCFStockForm, ClientForm, VehicleForm, VPForm, SalespersonForm, ClientContactForm, InternalTransportForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def home(request):
    return render(request, 'encomenda_veiculos/home.html')

class CustomLoginView(LoginView):
    template_name = 'encomenda_veiculos/login.html'
    # You can specify a redirect URL here, but it's better to use LOGIN_REDIRECT_URL in settings.py

class CustomLogoutView(LogoutView):
    # The LOGOUT_REDIRECT_URL from settings.py will be used for redirection
    pass

# Client Views
@method_decorator(login_required, name='dispatch')
class ClientListView(ListView):
    model = Client
    template_name = 'encomenda_veiculos/client_list.html'

@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = 'encomenda_veiculos/client_detail.html'

@method_decorator(login_required, name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'encomenda_veiculos/client_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

@method_decorator(login_required, name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'encomenda_veiculos/client_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

@method_decorator(login_required, name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'encomenda_veiculos/client_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:client_list')

# VP Views
@method_decorator(login_required, name='dispatch')
class VPListView(ListView):
    model = VP
    template_name = 'encomenda_veiculos/vp_list.html'

@method_decorator(login_required, name='dispatch')
class VPDetailView(DetailView):
    model = VP
    template_name = 'encomenda_veiculos/vp_detail.html'

@method_decorator(login_required, name='dispatch')
class VPCreateView(CreateView):
    model = VP
    form_class = VPForm
    template_name = 'encomenda_veiculos/vp_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

@method_decorator(login_required, name='dispatch')
class VPUpdateView(UpdateView):
    model = VP
    form_class = VPForm
    template_name = 'encomenda_veiculos/vp_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

@method_decorator(login_required, name='dispatch')
class VPDeleteView(DeleteView):
    model = VP
    template_name = 'encomenda_veiculos/vp_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:vp_list')

# OCFStock Views
@method_decorator(login_required, name='dispatch')
class OCFStockListView(ListView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_list.html'

@method_decorator(login_required, name='dispatch')
class OCFStockDetailView(DetailView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_detail.html'

@method_decorator(login_required, name='dispatch')
class OCFStockCreateView(CreateView):
    model = OCFStock
    form_class = OCFStockForm
    template_name = 'encomenda_veiculos/ocfstock_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

@method_decorator(login_required, name='dispatch')
class OCFStockUpdateView(UpdateView):
    model = OCFStock
    form_class = OCFStockForm
    template_name = 'encomenda_veiculos/ocfstock_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

@method_decorator(login_required, name='dispatch')
class OCFStockDeleteView(DeleteView):
    model = OCFStock
    template_name = 'encomenda_veiculos/ocfstock_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:ocfstock_list')

# Salesperson Views
@method_decorator(login_required, name='dispatch')
class SalespersonListView(ListView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_list.html'

@method_decorator(login_required, name='dispatch')
class SalespersonDetailView(DetailView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_detail.html'

@method_decorator(login_required, name='dispatch')
class SalespersonCreateView(CreateView):
    model = Salesperson
    form_class = SalespersonForm
    template_name = 'encomenda_veiculos/salesperson_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

@method_decorator(login_required, name='dispatch')
class SalespersonUpdateView(UpdateView):
    model = Salesperson
    form_class = SalespersonForm
    template_name = 'encomenda_veiculos/salesperson_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

@method_decorator(login_required, name='dispatch')
class SalespersonDeleteView(DeleteView):
    model = Salesperson
    template_name = 'encomenda_veiculos/salesperson_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:salesperson_list')

# ClientContact Views
@method_decorator(login_required, name='dispatch')
class ClientContactListView(ListView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_list.html'

@method_decorator(login_required, name='dispatch')
class ClientContactDetailView(DetailView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_detail.html'

@method_decorator(login_required, name='dispatch')
class ClientContactCreateView(CreateView):
    model = ClientContact
    form_class = ClientContactForm
    template_name = 'encomenda_veiculos/clientcontact_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

@method_decorator(login_required, name='dispatch')
class ClientContactUpdateView(UpdateView):
    model = ClientContact
    form_class = ClientContactForm
    template_name = 'encomenda_veiculos/clientcontact_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

@method_decorator(login_required, name='dispatch')
class ClientContactDeleteView(DeleteView):
    model = ClientContact
    template_name = 'encomenda_veiculos/clientcontact_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:clientcontact_list')

# InternalTransport Views
@method_decorator(login_required, name='dispatch')
class InternalTransportListView(ListView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_list.html'

@method_decorator(login_required, name='dispatch')
class InternalTransportDetailView(DetailView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_detail.html'

@method_decorator(login_required, name='dispatch')
class InternalTransportCreateView(CreateView):
    model = InternalTransport
    form_class = InternalTransportForm
    template_name = 'encomenda_veiculos/internaltransport_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')

@method_decorator(login_required, name='dispatch')
class InternalTransportUpdateView(UpdateView):
    model = InternalTransport
    form_class = InternalTransportForm
    template_name = 'encomenda_veiculos/internaltransport_form.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')

@method_decorator(login_required, name='dispatch')
class InternalTransportDeleteView(DeleteView):
    model = InternalTransport
    template_name = 'encomenda_veiculos/internaltransport_confirm_delete.html'
    success_url = reverse_lazy('Encomenda_Veiculos:internaltransport_list')
