from django.db    import models
from users.models import User

class Product(models.Model):
    size           = models.IntegerField(max_length=100)
    description    = models.CharField(max_length=100)
    price          = models.DecimalField(max_digits=6, decimal_places=2)
    category       = models.ForeignKey('Category', on_delete=models.CASCADE)
    alcohol_degree = models.ForeignKey('Alcohol_Degree', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class product_Image(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class category_Image(models.Model):
    image_url = models.URLField(max_length=2000)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_images'

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

class Alcohol_Degree(models.Model):
    percent = models.IntegerField(max_length=500)

    class Meta:
        db_table = 'alcohol_degrees'

class Finger_food(models.Model):
    name     = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'finger_foods'

class finger_food_Image(models.Model):
    image_url   = models.URLField(max_length=2000)
    finger_food = models.ForeignKey(Finger_food, on_delete=models.CASCADE)

    class Meta:
        db_table = 'finger_food_images'

class Cart(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      
    class Meta:
        db_table = 'carts'