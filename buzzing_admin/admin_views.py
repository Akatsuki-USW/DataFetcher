from django.views import View
from django.http import JsonResponse
from .models import Users
import jwt
import bcrypt
from django_secrets import JWT_SECRET_KEY, ALGORITHM
import json
from django.views.decorators.csrf import csrf_exempt #csrf token 비활성화
from django.utils.decorators import method_decorator  #csrf token 비활성화

@method_decorator(csrf_exempt, name='dispatch')  #csrf token 비활성화
class AdminLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        social_email = data.get('social_email')
        password = data.get('password')

        if not all([social_email, password]):
            return JsonResponse({'message': 'INVALID_DATA'}, status=400)

        try:
            user = Users.objects.get(social_email=social_email)

            if user.role != 'ROLE_ADMIN':
                return JsonResponse({'message': 'NO_PERMISSION'}, status=403)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                payload = {"user_id": user.user_id}
                token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'AccessToken': token}, status=200)

            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except Users.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
