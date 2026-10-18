import jwt
from django.http import JsonResponse
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        open_paths = ['/', '/login/', '/hello/', '/admin/']

        if request.path in open_paths or request.path.startswith('/admin/'):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'message': 'Thiếu Token xác thực!'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_info = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token đã hết hạn!'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Token không hợp lệ!'}, status=401)

        return self.get_response(request)