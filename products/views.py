
import json, re, random
from unicodedata      import name

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from random           import randint
from products.models  import Product, ProductImage, Category, CategoryImage

class ProductListView(View):
    def get(self, request):
        try:
            category  = request.GET.get('category', None)
            searching = request.GET.get('name', None)

            category       = Category.objects.get(id=1)
            category_image = CategoryImage.objects.get(id=1)

            products       = Product.objects.get(id=1)
            products       = Product.objects.filter(name__icontains=searching) if searching else products
            products_image = ProductImage.objects.get(id=1)
            product_random = random.choice(list(products.items()))
            product_random = json.dumps(product_random)
            product_random = Product.objects.filter(Q(category_id=category)) if category else products

            product_list = [{
                'category_image'  : category_image.image_url,
                'category'        : category,
                'product_image'   : products_image.image_url,
                'name'            : products.name,
                'price'           : products.price,
                'description_tag' : products.description_tag
            }]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status = 400)
        return JsonResponse({'message': 'SUCCESS', 'product_list' : product_list}, status = 200)
