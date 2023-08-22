import jwt

from django.http import JsonResponse

from django_secrets import JWT_SECRET_KEY, ALGORITHM
from buzzing_admin.models import Users

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)

        if token is None:
            return JsonResponse({'error': 'ENTER_THE_TOKEN'}, status=401)

        token = request.headers.get('Authorization', None)
        if token is None:
            return JsonResponse({'error': 'ENTER_THE_TOKEN'}, status=401)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)

            if Users.objects.filter(id=payload['user_id']).exists():
                request.user = Users.objects.get(id=payload['user_id'])
                return func(self, request, *args, **kwargs)

            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        except jwt.InvalidSignatureError:
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'EXPIRED_SIGNATURE'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)

    return wrapper
