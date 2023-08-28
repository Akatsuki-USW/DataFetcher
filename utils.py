import jwt

from django.http import JsonResponse

from django_secrets import JWT_SECRET_KEY, ALGORITHM
from buzzing_admin.models import Users


def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        token_header = request.headers.get('Authorization', None)

        if not token_header:
            return JsonResponse({'error': 'ENTER_THE_TOKEN'}, status=401)

        # Bearer 제거
        token = token_header.split(' ')[1] if 'Bearer' in token_header else token_header

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)

            if Users.objects.filter(user_id=payload['user_id']).exists():
                request.user = Users.objects.get(user_id=payload['user_id'])
                print(payload)
                return func(self, request, *args, **kwargs)

            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        except jwt.InvalidSignatureError:
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'EXPIRED_SIGNATURE'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)

    return wrapper

