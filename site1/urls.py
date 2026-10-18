from django.contrib import admin
from django.urls import path
from api.views import login_view, hello_world, auth_view, product_list, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),
    path('hello/', hello_world),
    path('auth', auth_view),
    path('auth/', auth_view),
    # Product Management
    path('products', product_list),
    path('products/', product_list),
    path('products/<int:id>', product_detail),
    path('products/<int:id>/', product_detail),
]