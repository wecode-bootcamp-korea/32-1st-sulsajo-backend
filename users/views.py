
import json, re, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User
from users.validation import Validation
from django.core.exceptions import ValidationError

class SignupView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            Validation.email_validate(email)
            Validation.password_validate(password)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' :'ALREADY_EXISTS_EMAIL'}, status=400)

            hashed_password = bcrypt.hashpw((password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email     = data['email'],
                password  = hashed_password,
                name      = data['name'],
                nick_name = data['nick_name']
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValidationError:
            return JsonResponse({'message':'Validation_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])

            hashed_password = user.password.encode('utf-8')
            access_token    = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password):
                return JsonResponse({'message': "INVALID_USER"}, status=401)
            
            return JsonResponse({'message':'SUCCESS', 'token': access_token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=404)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)