import jwt
from django.http import JsonResponse
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Các đường dẫn công khai (không cần kiểm tra Token)
        open_paths = ['/', '/login/'] 

        if request.path in open_paths:
            return self.get_response(request)

        # Lấy token từ Header Authorization (Dạng: Bearer <token>)
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'message': 'Thiếu Token xác thực!'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            # Giải mã và xác thực Token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_info = payload  # Đính kèm thông tin user vào request
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token đã hết hạn!'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Token không hợp lệ!'}, status=401)

        return self.get_response(request)