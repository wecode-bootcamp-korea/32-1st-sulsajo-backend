from django.urls import path
from products.views import DetailProductView, DetailCommentView

urlpatterns = [
    path('/detailproduct', DetailProductView.as_view()),
    path('/detailcomment', DetailCommentView.as_view())
    ]