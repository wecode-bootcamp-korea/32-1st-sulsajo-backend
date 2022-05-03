import json, re

from django.shortcuts import render

from django.views     import View
from django.http      import JsonResponse, HttpResponse

from products.models  import Product, ProductImage, Category, CategoryImage, Comment, AlcoholType, FingerFood, OrderItem, Taste
from users.decorator  import log_in_decorator
from json.decoder     import JSONDecodeError

class DetailProductView(View):
    def get(self, request, product_id):
        try:
            products = Product.objects.filter(id = product_id)

            product_detail = [{
                'id'                 : product.id,
                'size'               : product.size,
                'name'               : product.name,
                'description_detail' : product.description_detail,
                'description_tag'    : product.description_tag,
                'price'              : product.price,
                'alcohol_percentage' : product.alcohol_percentage,
                'category'           : product.category.name,
                'product_image'      : [{
                    'id' : product_image.id,
                    'image_url' : product_image.image_url
                    } for product_image in product.productimage_set.all()],
                'taste'              : [{
                    'id'              : taste.id,
                    'spiceness'       : taste.spiceness,
                    'savory'          : taste.savory,
                    'refreshness'     : taste.refreshness,
                    'taste_intensity' : taste.taste_intensity,
                    'sweetness'       : taste.sweetness
                    } for taste in product.category.taste_set.all()],
                'finger_food'        : [{
                    'id'        : finger_food.id,
                    'name'      : finger_food.name,
                    'image_url' : finger_food.image_url
                    } for finger_food in product.category.fingerfood_set.all()]
                    } for product in products]

        except Product.DoesNotExist:
            return JsonResponse({'message':'VALUE_ERROR'}, status = 404)
        return JsonResponse({
            "message" : "상세페이지 제품 관련 데이터",
            "product_detail": product_detail
            },
            status = 200)

class DetailCommentView(View):
    @log_in_decorator
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user
            content      = data.get('content', None)
            product_name = data.get('product_name', None)
            created_at   = data.get('created_at', None)
            
            Comment.objects.create(
                content      = content,
                user         = user,
                product_name = product_name,
                created_at   = created_at
                )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class DetailCommentDeleteView(View):
    @log_in_decorator
    def delete(self, request, comment_id):
        user = request.user

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'message':'COMMENT_DOES_NOT_EXIST'}, status=404)

        comment = Comment.objects.get(id=comment_id)

        if user != comment.user:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        Comment.objects.filter(id=comment.id).delete()
        return JsonResponse({'message': 'SUCCESS'}, status=200)

class SubscribeView(View):
    def get(self, request, product_id):
        try:
            products = Product.objects.filter(id = product_id)

            subscribe_detail = [({
                'id'                 : product.id,
                'name'               : product.name,
                'product_image'      : product.productimage_set.first().image_url,
                'description_detail' : product.description_detail,
                'price'              : product.price,
                'alcohol_percentage' : product.alcohol_percentage,
                'description_tag'    : product.description_tag,
                'taste'              : [{
                    'id'              : taste.id,
                    'spiceness'       : taste.spiceness,
                    'savory'          : taste.savory,
                    'refreshness'     : taste.refreshness,
                    'taste_intensity' : taste.taste_intensity,
                    'sweetness'       : taste.sweetness
                    } for taste in product.category.taste_set.all()]
            })for product in products]

        except Product.DoesNotExist:
            return JsonResponse({'message':'VALUE_ERROR'}, status = 404)
        return JsonResponse({
            "message" : '구독페이지 제품 관련 데이터',
            'subscribe_detail': subscribe_detail
            },
            status = 200)

class ProductListView(View):
    def get(self, request):
        try:
            category       = request.GET.get('category', None)
            category_image = CategoryImage.objects.get(id=1)
            category_list  = [{
                'category_image' : category_image.image_url,
                'category'       : Product.category_set.name
            }]

            products_image   = ProductImage.objects.all()
            products         = Product.objects.all()
            searching        = request.GET.get('name', None)
            products         = Product.objects.filter(name__icontains=searching) if searching else products
            product_random   = Product.objects.order_by('?')[:12]
            product_random   = Product.objects.filter(category_id__icontains=product_random)

            product_list = [{
                'product_image'   : products_image.image_url,
                'name'            : products.name,
                'price'           : products.price,
                'description_tag' : products.description_tag
            }]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status = 400)
        return JsonResponse({
            'message': 'SUCCESS', 'category_list': category_list,'product_list' : product_list}, status = 200
            )