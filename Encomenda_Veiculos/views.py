from django.shortcuts import render
from .models import OCFStock

# Create your views here.

def vehicle_stock_list(request):
    """
    A view to display a list of all vehicles in the OCF stock.
    """
    # Fetch all stock entries.
    # .select_related() is a performance optimization that pre-fetches related
    # vehicle and VP data in a single database query.
    stock_items = OCFStock.objects.select_related('vehicle', 'vehicle__vp').all()

    context = {
        'stock_items': stock_items
    }
    # The template file 'encomenda_veiculos/stock_list.html' doesn't exist yet.
    # We will create it in the next step.
    return render(request, 'encomenda_veiculos/stock_list.html', context)
