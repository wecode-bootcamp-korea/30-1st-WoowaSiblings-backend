from django.urls import path

from products.views import ProductListView
from products.views import ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]