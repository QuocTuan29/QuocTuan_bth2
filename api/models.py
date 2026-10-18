from django.db import models


class User(models.Model):
    IdUser = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=255, unique=True)
    Password = models.CharField(max_length=255)
    Token = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.UserName


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'