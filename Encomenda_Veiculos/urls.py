from django.urls import path
from . import views

app_name = 'Encomenda_Veiculos'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('set_language/', views.set_language, name='set_language'),

    path('', views.home, name='home'),
    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # VP URLs
    path('vps/', views.VPListView.as_view(), name='vp_list'),
    path('vps/<int:pk>/', views.VPDetailView.as_view(), name='vp_detail'),
    path('vps/create/', views.VPCreateView.as_view(), name='vp_create'),
    path('vps/<int:pk>/update/', views.VPUpdateView.as_view(), name='vp_update'),
    path('vps/<int:pk>/delete/', views.VPDeleteView.as_view(), name='vp_delete'),

    # OCFStock URLs
    path('ocfstocks/', views.OCFStockListView.as_view(), name='ocfstock_list'),
    path('ocfstocks/<int:pk>/', views.OCFStockDetailView.as_view(), name='ocfstock_detail'),
    path('ocfstocks/create/', views.OCFStockCreateView.as_view(), name='ocfstock_create'),
    path('ocfstocks/<int:pk>/update/', views.OCFStockUpdateView.as_view(), name='ocfstock_update'),
    path('ocfstocks/<int:pk>/delete/', views.OCFStockDeleteView.as_view(), name='ocfstock_delete'),

    # Salesperson URLs
    path('salespersons/', views.SalespersonListView.as_view(), name='salesperson_list'),
    path('salespersons/<int:pk>/', views.SalespersonDetailView.as_view(), name='salesperson_detail'),
    path('salespersons/create/', views.SalespersonCreateView.as_view(), name='salesperson_create'),
    path('salespersons/<int:pk>/update/', views.SalespersonUpdateView.as_view(), name='salesperson_update'),
    path('salespersons/<int:pk>/delete/', views.SalespersonDeleteView.as_view(), name='salesperson_delete'),

    # ClientContact URLs
    path('clientcontacts/', views.ClientContactListView.as_view(), name='clientcontact_list'),
    path('clientcontacts/<int:pk>/', views.ClientContactDetailView.as_view(), name='clientcontact_detail'),
    path('clientcontacts/create/', views.ClientContactCreateView.as_view(), name='clientcontact_create'),
    path('clientcontacts/<int:pk>/update/', views.ClientContactUpdateView.as_view(), name='clientcontact_update'),
    path('clientcontacts/<int:pk>/delete/', views.ClientContactDeleteView.as_view(), name='clientcontact_delete'),

    # InternalTransport URLs
    path('internaltransports/', views.InternalTransportListView.as_view(), name='internaltransport_list'),
    path('internaltransports/<int:pk>/', views.InternalTransportDetailView.as_view(), name='internaltransport_detail'),
    path('internaltransports/create/', views.InternalTransportCreateView.as_view(), name='internaltransport_create'),
    path('internaltransports/<int:pk>/update/', views.InternalTransportUpdateView.as_view(), name='internaltransport_update'),
    path('internaltransports/<int:pk>/delete/', views.InternalTransportDeleteView.as_view(), name='internaltransport_delete'),
]
