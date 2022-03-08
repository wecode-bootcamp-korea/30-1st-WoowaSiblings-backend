from django.urls import path

from products.views import DetailView

urlpatterns = [
    path('/<int:product_id>', DetailView.as_view())
]