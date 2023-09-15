from django.views.generic import ListView
from .models import Product

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "home.html"