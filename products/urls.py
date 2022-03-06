from django.urls import path

from products.views import DetailView

urlpatterns = [
    path('/detail', DetailView.as_view())
]