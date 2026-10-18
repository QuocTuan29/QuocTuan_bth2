"""
URL configuration for site1 project.
"""
from django.contrib import admin
from django.urls import path

from api.views import login_view, hello_world, auth_view, product_list, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),                       # URL Đăng nhập: localhost:8000/
    path('hello/', hello_world),                # URL Hello World
    path('auth', auth_view),                    # URL Xác thực Token: localhost:8000/auth
    path('auth/', auth_view),
    # Product Management APIs
    path('products', product_list),             # GET all / POST create
    path('products/', product_list),
    path('products/<int:id>', product_detail),  # GET / PUT / DELETE by id
    path('products/<int:id>/', product_detail),
]
