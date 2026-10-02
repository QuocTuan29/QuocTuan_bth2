from django.shortcuts import render

# Create your views here.
import base64
import jwt
import datetime
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

SECRET_KEY = 'django-insecure-h@jkhug1+fp8d9=(6rl!*0_1l*q9jq&rswqt0^5u%d&z0s$w14'  # Có thể dùng settings.SECRET_KEY

# 1. API Đăng nhập (localhost:8000/)
@api_view(['POST'])
def login_view(request):
    username = request.data.get('userName')
    password_encoded = request.data.get('password')  # Client gửi mật khẩu mã hóa Base64

    if not username or not password_encoded:
        return Response({'message': 'Thiếu username hoặc password'}, status=status.HTTP_400_BAD_REQUEST)

    # Giải mã Base64 từ Client gửi lên
    try:
        decoded_bytes = base64.b64decode(password_encoded)
        password_plain = decoded_bytes.decode('utf-8')
    except Exception:
        password_plain = password_encoded # Nếu client truyền raw text

    # Kiểm tra trong DB (Lưu ý: Thực tế nên hash password)
    try:
        user = User.objects.get(UserName=username, Password=password_plain)
    except User.DoesNotExist:
        return Response({'message': 'Tài khoản hoặc mật khẩu không chính xác'}, status=status.HTTP_401_UNAUTHORIZED)

    # Sinh mã JWT Token (thời hạn 1 ngày)
    payload = {
        'id': user.IdUser,
        'username': user.UserName,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    # Lưu Token vào DB
    user.Token = token
    user.save()

    return Response({
        'message': 'Đăng nhập thành công',
        'token': token
    })

# 2. API Hello World (từ bài 1)
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello World'})

# 3. API Xác thực localhost:8000/auth
@api_view(['GET'])
def auth_view(request):
    # Lấy thông tin user đã được gán bởi Middleware
    user_info = getattr(request, 'user_info', None)
    return Response({
        'message': 'Xác thực token thành công!',
        'user': user_info
    })
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY