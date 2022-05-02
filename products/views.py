import json, re

from django.shortcuts import render

from django.views     import View
from django.http      import JsonResponse, HttpResponse

from products.models  import Product, ProductImage, Category, CategoryImage, Comment, AlcoholType, FingerFood, FingerFoodImage, OrderItem, Taste
from users.decorator  import log_in_decorator

class DetailProductView(View):
    def get(self, request, product_id):
        try:
            products           = Product.objects.get(id = product_id)
            categories         = Category.objects.all()
            product_images     = ProductImage.objects.all()
            tastes             = Taste.objects.all()
            finger_foods       = FingerFood.objects.all()
            finger_food_images = FingerFoodImage.objects.all()

            product_detail = [({
                'id'                 : product.products.id,
                'size'               : product.products.size,
                'name'               : product.products.name,
                'description_detail' : product.products.description_detail,
                'description_tag'    : product.products.description_tag,
                'price'              : product.products.price,
                'alcohol_percentage' : product.alcohol_percentage,
                'category'           : [category.name for category in product.category.all()],
                'product_image'      : [image.image_url for image in product.productimage_set.all()],
                'taste'              : [[taste.spiceness for taste in product.category.taste_set.all()],
                                        [taste.savory for taste in product.category.taste_set.all()],
                                        [taste.refreshness for taste in product.category.taste_set.all()],
                                        [taste.taste_intensity for taste in product.category.taste_set.all()],
                                        [taste.sweetness for taste in product.category.taste_set.all()]],
                'finger_food'        : [fingerfood.name for fingerfood in product.category.fingerfood_set.all()],
                'finger_food_image'  : [fingerfoodimage.image_url for fingerfoodimage in product.category.fingerfood.fingerfoodimage_set.all()]
            }) for product in products] 

        except Product.DoesNotExist:
            return HttpResponse(status = 404)
        return JsonResponse({
            "message" : '상세페이지 제품 관련 데이터',
            'product_detail': product_detail
            },
            status = 200)

class DetailCommentView(View):
    @log_in_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            content    = data.get('content', None)
            
            Comment.objects.create(
                content = content,
                user    = user,
                )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)