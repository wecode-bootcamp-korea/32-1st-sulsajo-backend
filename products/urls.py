from django.urls import path
from products.views import DetailProductView, DetailCommentView, ProductListView, DetailCommentDeleteView, SubscribeView

urlpatterns = [
    path('/detailproduct/<int:product_id>', DetailProductView.as_view()),
    path('/detailcomment', DetailCommentView.as_view()),
    path('/productlist', ProductListView.as_view()),
    path('/detailcommentdelete', DetailCommentDeleteView.as_view()),
    path('/subscribe/<int:product_id>', SubscribeView.as_view())
    ]