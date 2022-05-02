
import json, re, random

from django.shortcuts import render

from django.views     import View
from django.http      import JsonResponse
from random           import randint

from products.models  import Product, ProductImage, Category, CategoryImage, Comment, AlcoholType, FingerFood, FingerFoodImage, OrderItem, Taste

class ProductListView(View):
    def get(self, request):
        try:
            category       = request.GET.get('category', None)
            category_image = CategoryImage.objects.all()
            category_list  = [{
                'category_image' : category_image.image_url,
                'category'       : category.name
            }]

            products_image  = ProductImage.objects.all()
            products        = Product.objects.all()
            searching       = request.GET.get('name', None)
            products        = Product.objects.filter(name__icontains=searching) if searching else products
            random_product  = Product.objects.values_list('pk', flat=True)
            random_product  = Product.objects.filter(id__in=random.sample(random_product, 12))
            random_category = Product.objects.filter(category_id__icontains=random_product)

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
