from django.urls import path
from products.views import ProductView, CommentView, SubscribeView

urlpatterns = [
    path('/product/<int:product_id>', ProductView.as_view()),
    path('/product/<int:product_id>/comment', CommentView.as_view()),
    path('/subscribe/<int:product_id>', SubscribeView.as_view())
    ]