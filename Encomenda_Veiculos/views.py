import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import OCFStock, Client, Vehicle, VP, Salesperson, ClientContact, InternalTransport
from .forms import OCFStockForm, ClientForm, VehicleForm, VPForm, SalespersonForm, ClientContactForm, InternalTransportForm, ImportFileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from .forms import ImportFileForm
import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
    return render(request, 'encomenda_veiculos/home.html')

@login_required
def import_data(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Get the uploaded file
                excel_file = request.FILES['file']

                # Read Excel file into pandas DataFrame
                df = pd.read_excel(excel_file, sheet_name=0)

                # Optional: Clean column names (remove extra spaces)
                df.columns = df.columns.str.strip()

                # Counters for tracking imports
                success_count = 0
                error_count = 0
                skipped_count = 0
                updated_count = 0
                created_count = 0

                # Use transaction to ensure data consistency
                with transaction.atomic():
                    # Iterate through DataFrame rows
                    for index, row in df.iterrows():
                        try:
                            # Extract VAN and VP Code
                            van_value = row.get('VAN Testo')
                            vp_code_value = row.get('VP Codice')

                            if pd.isna(van_value) or pd.isna(vp_code_value):
                                skipped_count += 1
                                logger.warning(f"Row {index}: Missing VAN or VP Code, skipping")
                                continue

                            # Convert VAN to integer
                            try:
                                van_int = int(van_value)
                            except (ValueError, TypeError):
                                skipped_count += 1
                                logger.warning(f"Row {index}: Invalid VAN value '{van_value}', skipping")
                                continue

                            # Get or create VP
                            vp, vp_created = VP.objects.get_or_create(
                                vp_code=str(vp_code_value),
                                defaults={
                                    'variant': row.get('Gruppo Alternativo 1'),
                                    'version': row.get('Gruppo Alternativo 2'),
                                    'engine_code': row.get('Motore_V'),
                                    'gama': row.get('NIC Livello 1'),
                                    'modelo': row.get('NIC Livello 5'),
                                    'cabina': row.get('CT - Descrizione estesa codice cabina comfort'),
                                    'motor': row.get('EP - Descrizione estesa potenza motore'),
                                    'gearbox': row.get('GT - Descrizione estesa tipo gearbox'),
                                    'wheelbase': row.get('WB - Descrizione estesa interasse'),
                                    'hi': row.get('HI - Descrizione estesa compartimento di carico'),
                                    'color_code_numeric': int(row.get('Colore_Codice (Numerico)')) if pd.notna(
                                        row.get('Colore_Codice (Numerico)')) else None,
                                    'color_desc': row.get('Colore_Descrizione Estesa'),
                                }
                            )

                            # ============================================================
                            # UPDATE VP IF EXISTS - Review these fields to update
                            # ============================================================
                            if not vp_created:
                                # TODO: Review which VP fields should be updated
                                # Currently: NO VP fields are being updated on existing records
                                # Uncomment below to update specific fields:

                                # vp.variant = row.get('Gruppo Alternativo 1') or vp.variant
                                # vp.version = row.get('Gruppo Alternativo 2') or vp.version
                                # vp.engine_code = row.get('Motore_V') or vp.engine_code
                                # vp.gama = row.get('NIC Livello 1') or vp.gama
                                # vp.modelo = row.get('NIC Livello 5') or vp.modelo
                                # vp.cabina = row.get('CT - Descrizione estesa codice cabina comfort') or vp.cabina
                                # vp.motor = row.get('EP - Descrizione estesa potenza motore') or vp.motor
                                # vp.gearbox = row.get('GT - Descrizione estesa tipo gearbox') or vp.gearbox
                                # vp.wheelbase = row.get('WB - Descrizione estesa interasse') or vp.wheelbase
                                # vp.hi = row.get('HI - Descrizione estesa compartimento di carico') or vp.hi
                                # vp.color_code_numeric = int(row.get('Colore_Codice (Numerico)')) if pd.notna(row.get('Colore_Codice (Numerico)')) else vp.color_code_numeric
                                # vp.color_desc = row.get('Colore_Descrizione Estesa') or vp.color_desc

                                # vp.save()
                                logger.info(f"VP already exists: {vp.vp_code} (no updates)")
                            # ============================================================

                            # Get or create Vehicle
                            vehicle, vehicle_created = Vehicle.objects.get_or_create(
                                van=van_int,
                                defaults={
                                    'vin': row.get('VIN_V') if pd.notna(row.get('VIN_V')) else None,
                                    'country': row.get('Ubicazione_Paese'),
                                    'vp': vp,
                                }
                            )

                            # ============================================================
                            # UPDATE VEHICLE IF EXISTS - Review these fields to update
                            # ============================================================
                            if not vehicle_created:
                                # TODO: Review which Vehicle fields should be updated
                                # Currently: Only VP reference is updated on existing vehicles

                                vehicle.vp = vp  # Always update VP reference

                                # Uncomment below to update other fields:
                                # vehicle.vin = row.get('VIN_V') if pd.notna(row.get('VIN_V')) else vehicle.vin
                                # vehicle.country = row.get('Ubicazione_Paese') or vehicle.country
                                # vehicle.plate = ...  # Add if needed
                                # vehicle.registration_date = ...  # Add if needed
                                # vehicle.lot = ...  # Add if needed
                                # vehicle.production_year = ...  # Add if needed

                                vehicle.save()
                                logger.info(f"Updated Vehicle: VAN {vehicle.van} (VP reference only)")
                            else:
                                created_count += 1
                            # ============================================================

                            # Get or create OCFStock
                            ocf_stock, ocf_created = OCFStock.objects.get_or_create(
                                vehicle=vehicle,
                                defaults={
                                    'has_client': bool(row.get('Flag NCF Stato')) if pd.notna(
                                        row.get('Flag NCF Stato')) else False,
                                    'client_assigned_date': pd.to_datetime(
                                        row.get('OCF Data Giorno')).date() if pd.notna(
                                        row.get('OCF Data Giorno')) else None,
                                    'channel': row.get('Canale Di Vendita_Descrizione'),
                                    'distributor': row.get('Canale Di Vendita Amministrativo_Descrizione Estesa'),
                                    'order_date': pd.to_datetime(
                                        row.get('Ordine Di Vendita Data Giorno')).date() if pd.notna(
                                        row.get('Ordine Di Vendita Data Giorno')) else None,
                                    'order_number': int(row.get('Ordine')) if pd.notna(row.get('Ordine')) else None,
                                    'client_name': row.get('Cliente_Nome'),
                                    'client_final': row.get('Nome Cliente (Destinatario Merci)'),
                                    'sold': row.get('Stato Fatturazione') == 'Sold' if pd.notna(
                                        row.get('Stato Fatturazione')) else False,
                                    'produced': row.get('Stato Produttivo') == 'Produced' if pd.notna(
                                        row.get('Stato Produttivo')) else False,
                                    'delivery_date': pd.to_datetime(
                                        row.get('Fattura Data Giorno_V')).date() if pd.notna(
                                        row.get('Fattura Data Giorno_V')) else None,
                                    'location': row.get('Ubicazione_Descrizione'),
                                    'location_date': pd.to_datetime(
                                        row.get('Location Data Giorno_V')).date() if pd.notna(
                                        row.get('Location Data Giorno_V')) else None,
                                    'warranty_start': pd.to_datetime(row.get('MAV Data Giorno_V')).date() if pd.notna(
                                        row.get('MAV Data Giorno_V')) else None,
                                    'notes': row.get('Elemento di testo'),
                                }
                            )

                            # ============================================================
                            # UPDATE OCFStock IF EXISTS - Review these fields to update
                            # ============================================================
                            if not ocf_created:
                                # TODO: Review which OCFStock fields should be updated
                                # Currently: ONLY "Stato Produttivo" (produced) field is updated

                                # ===== ACTIVE UPDATE: Stato Produttivo =====
                                stato_produttivo = row.get('Stato Produttivo')
                                if pd.notna(stato_produttivo):
                                    ocf_stock.produced = (stato_produttivo == 'Produced')
                                    logger.info(f"Updated 'produced' status for VAN {vehicle.van}: {stato_produttivo}")
                                # ===========================================

                                # Client/Order Information - Uncomment fields to update
                                # ocf_stock.has_client = bool(row.get('Flag NCF Stato')) if pd.notna(row.get('Flag NCF Stato')) else ocf_stock.has_client
                                # ocf_stock.client_assigned_date = pd.to_datetime(row.get('OCF Data Giorno')).date() if pd.notna(row.get('OCF Data Giorno')) else ocf_stock.client_assigned_date
                                # ocf_stock.channel = row.get('Canale Di Vendita_Descrizione') or ocf_stock.channel
                                # ocf_stock.distributor = row.get('Canale Di Vendita Amministrativo_Descrizione Estesa') or ocf_stock.distributor
                                # ocf_stock.order_date = pd.to_datetime(row.get('Ordine Di Vendita Data Giorno')).date() if pd.notna(row.get('Ordine Di Vendita Data Giorno')) else ocf_stock.order_date
                                # ocf_stock.order_number = int(row.get('Ordine')) if pd.notna(row.get('Ordine')) else ocf_stock.order_number
                                # ocf_stock.client_name = row.get('Cliente_Nome') or ocf_stock.client_name
                                # ocf_stock.client_final = row.get('Nome Cliente (Destinatario Merci)') or ocf_stock.client_final

                                # Status Fields - Uncomment fields to update
                                # ocf_stock.sold = row.get('Stato Fatturazione') == 'Sold' if pd.notna(row.get('Stato Fatturazione')) else ocf_stock.sold

                                # Delivery/Location - Uncomment fields to update
                                # ocf_stock.delivery_date = pd.to_datetime(row.get('Fattura Data Giorno_V')).date() if pd.notna(row.get('Fattura Data Giorno_V')) else ocf_stock.delivery_date
                                # ocf_stock.location = row.get('Ubicazione_Descrizione') or ocf_stock.location
                                # ocf_stock.location_date = pd.to_datetime(row.get('Location Data Giorno_V')).date() if pd.notna(row.get('Location Data Giorno_V')) else ocf_stock.location_date

                                # Warranty - Uncomment fields to update
                                # ocf_stock.warranty_start = pd.to_datetime(row.get('MAV Data Giorno_V')).date() if pd.notna(row.get('MAV Data Giorno_V')) else ocf_stock.warranty_start

                                # Notes - Uncomment fields to update
                                # ocf_stock.notes = row.get('Elemento di testo') or ocf_stock.notes

                                ocf_stock.save()
                                updated_count += 1
                            else:
                                created_count += 1
                            # ============================================================

                            success_count += 1

                        except Exception as e:
                            error_count += 1
                            logger.error(f"Error importing row {index}: {str(e)}")
                            continue

                # Success messages
                if created_count > 0:
                    messages.success(request, f'Successfully created {created_count} new records.')
                if updated_count > 0:
                    messages.info(request, f'Updated {updated_count} existing records (Stato Produttivo only).')
                if skipped_count > 0:
                    messages.info(request, f'Skipped {skipped_count} records (missing VAN or VP Code).')
                if error_count > 0:
                    messages.warning(request, f'Failed to import {error_count} records. Check logs for details.')

                return redirect(reverse_lazy('Encomenda_Veiculos:home'))

            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = ImportFileForm()

    return render(request, 'encomenda_veiculos/import_data.html', {'form': form})

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
