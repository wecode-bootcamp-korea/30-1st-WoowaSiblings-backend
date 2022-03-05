from django.urls    import path

from products.views import ProductListView

urlpatterns = [
    path('/productlist', ProductListView.as_view()),
]