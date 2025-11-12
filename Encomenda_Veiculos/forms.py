from django import forms
from .models import Salesperson, Client, ClientContact, VP, Vehicle, InternalTransport, OCFStock

class SalespersonForm(forms.ModelForm):
    class Meta:
        model = Salesperson
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['code']

class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = '__all__'

class VPForm(forms.ModelForm):
    class Meta:
        model = VP
        fields = '__all__'

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

class InternalTransportForm(forms.ModelForm):
    class Meta:
        model = InternalTransport
        fields = '__all__'

class OCFStockForm(forms.ModelForm):
    class Meta:
        model = OCFStock
        fields = '__all__'
