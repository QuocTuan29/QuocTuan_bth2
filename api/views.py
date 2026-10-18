import base64
import jwt
import datetime
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product

SECRET_KEY = settings.SECRET_KEY


# 1. API Đăng nhập
@api_view(['POST'])
def login_view(request):
    username = request.data.get('userName')
    password_encoded = request.data.get('password')

    if not username or not password_encoded:
        return Response({'message': 'Thiếu username hoặc password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded_bytes = base64.b64decode(password_encoded)
        password_plain = decoded_bytes.decode('utf-8')
    except Exception:
        password_plain = password_encoded

    try:
        user = User.objects.get(UserName=username, Password=password_plain)
    except User.DoesNotExist:
        return Response({'message': 'Tài khoản hoặc mật khẩu không chính xác'}, status=status.HTTP_401_UNAUTHORIZED)

    payload = {
        'id': user.IdUser,
        'username': user.UserName,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    user.Token = token
    user.save()

    return Response({
        'message': 'Đăng nhập thành công',
        'token': token
    })


# 2. API Hello World
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello World'})


# 3. API Xác thực
@api_view(['GET'])
def auth_view(request):
    user_info = getattr(request, 'user_info', None)
    return Response({
        'message': 'Xác thực token thành công!',
        'user': user_info
    })


# ==================== PRODUCT MANAGEMENT ====================

def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'quantity': product.quantity,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'updated_at': product.updated_at.isoformat() if product.updated_at else None,
    }


# GET /products  - Lấy danh sách
# POST /products - Thêm mới
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('-created_at')
        data = [product_to_dict(p) for p in products]
        return Response({
            'message': 'Lấy danh sách sản phẩm thành công',
            'count': len(data),
            'products': data
        })

    elif request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description', '')
        price = request.data.get('price')
        quantity = request.data.get('quantity', 0)

        if not name or price is None:
            return Response(
                {'message': 'Thiếu trường bắt buộc: name và price'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            price = float(price)
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response(
                {'message': 'price phải là số và quantity phải là số nguyên'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )
        return Response({
            'message': 'Thêm sản phẩm thành công',
            'product': product_to_dict(product)
        }, status=status.HTTP_201_CREATED)


# GET /products/<id>    - Chi tiết
# PUT /products/<id>    - Cập nhật
# DELETE /products/<id> - Xóa
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            {'message': f'Không tìm thấy sản phẩm với id={id}'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response({
            'message': 'Lấy thông tin sản phẩm thành công',
            'product': product_to_dict(product)
        })

    elif request.method == 'PUT':
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        quantity = request.data.get('quantity')

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            try:
                product.price = float(price)
            except (ValueError, TypeError):
                return Response({'message': 'price phải là số'}, status=status.HTTP_400_BAD_REQUEST)
        if quantity is not None:
            try:
                product.quantity = int(quantity)
            except (ValueError, TypeError):
                return Response({'message': 'quantity phải là số nguyên'}, status=status.HTTP_400_BAD_REQUEST)

        product.save()
        return Response({
            'message': 'Cập nhật sản phẩm thành công',
            'product': product_to_dict(product)
        })

    elif request.method == 'DELETE':
        product_id = product.id
        product.delete()
        return Response({'message': f'Xóa sản phẩm id={product_id} thành công'})