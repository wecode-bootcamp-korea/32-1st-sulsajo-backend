from django.urls import path
from products.views import ProductDetailView, CommentView, SubscribeView, ProductListView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/comment', CommentView.as_view()),
    path('/<int:product_id>/comment/<int:comment_id>', CommentView.as_view()),
    path('/<int:product_id>/subscribe', SubscribeView.as_view()),
    path('/list', ProductListView.as_view())
    ]
