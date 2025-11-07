from django.urls import path
from . import views

app_name = 'Encomenda_Veiculos'

urlpatterns = [
    # This maps the URL '/stock/' to our new view function.
    path('stock/', views.vehicle_stock_list, name='vehicle_stock_list'),
]