from django.urls import path

from products.views import LikeView

urlpatterns = [
    path('/like', LikeView.as_view())
]