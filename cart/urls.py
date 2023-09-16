from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
]