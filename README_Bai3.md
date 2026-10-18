# Bài thực hành số 3 – Dịch vụ Quản lý Sản phẩm (Product Management)

## Mục tiêu
- Xây dựng dịch vụ quản lý sản phẩm (CRUD) độc lập theo kiến trúc SOA.
- Chạy trên cổng riêng (`localhost:8001`) với database riêng (SQLite).
- Xác thực qua JWT token từ dịch vụ Auth (Bài thực hành số 2).

## Cài đặt & Chạy

```bash
# 1. Cài dependencies
pip install django djangorestframework pyjwt

# 2. Tạo database
python manage.py makemigrations api
python manage.py migrate

# 3. Tạo user mẫu
python manage.py shell -c "from api.models import User; User.objects.get_or_create(UserName='admin', defaults={'Password': 'admin123'})"

# 4. Chạy server trên cổng 8001
python manage.py runserver 8001
```

## API Endpoints

### Xác thực
| Method | URL | Mô tả | Auth |
|--------|-----|-------|------|
| POST | `/` | Đăng nhập, nhận JWT token | Không |
| GET | `/auth` | Kiểm tra token | Bearer Token |

### Quản lý sản phẩm
| Method | URL | Mô tả | Auth |
|--------|-----|-------|------|
| GET | `/products` | Lấy danh sách tất cả sản phẩm | Bearer Token |
| POST | `/products` | Thêm sản phẩm mới | Bearer Token |
| GET | `/products/{id}` | Lấy chi tiết 1 sản phẩm | Bearer Token |
| PUT | `/products/{id}` | Cập nhật sản phẩm | Bearer Token |
| DELETE | `/products/{id}` | Xóa sản phẩm | Bearer Token |

## Ví dụ sử dụng (Thunder Client / curl)

### 1. Đăng nhập
```
POST http://localhost:8001/
Content-Type: application/json

{
  "userName": "admin",
  "password": "admin123"
}
```

### 2. Thêm sản phẩm
```
POST http://localhost:8001/products
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Laptop Dell",
  "description": "Laptop cao cấp",
  "price": 25000000,
  "quantity": 10
}
```

### 3. Lấy danh sách
```
GET http://localhost:8001/products
Authorization: Bearer <token>
```

### 4. Lấy chi tiết
```
GET http://localhost:8001/products/1
Authorization: Bearer <token>
```

### 5. Cập nhật
```
PUT http://localhost:8001/products/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Laptop Dell XPS 15",
  "price": 27000000,
  "quantity": 8
}
```

### 6. Xóa
```
DELETE http://localhost:8001/products/1
Authorization: Bearer <token>
```

## Cấu trúc bảng products

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| id | INT (PK) | ID duy nhất |
| name | VARCHAR(255) | Tên sản phẩm |
| description | TEXT | Mô tả |
| price | DECIMAL(10,2) | Giá |
| quantity | INT | Số lượng kho |
| created_at | TIMESTAMP | Ngày tạo |
| updated_at | TIMESTAMP | Ngày cập nhật |

## Luồng hoạt động tóm tắt

1. Client đăng nhập → nhận JWT token.
2. Client gắn `Authorization: Bearer <token>` khi gọi API sản phẩm.
3. JWTMiddleware kiểm tra token trước khi vào view.
4. View xử lý nghiệp vụ CRUD và trả JSON.

## Công nghệ
- Django + Django REST Framework
- PyJWT (HS256)
- SQLite
- Cổng 8001
