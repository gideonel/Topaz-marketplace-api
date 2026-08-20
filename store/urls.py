"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from market.views import (
    get_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    create_batch_products,
    delete_all_products
)

#Swagger and Redoc documentation

schema_view = get_schema_view(
    openapi.Info(
        title="Store Project API",
        default_version='v1',
        description="API documentation for the Store Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lordgideonel@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('products/', get_products, name='get-products'),
    path('products/<int:id>/', get_product_by_id, name='get-product-by-id'),
    path('products/create/', create_product, name='create-product'),
    path('products/<int:id>/update/', update_product, name='update-product'),
    path('products/<int:id>/delete/', delete_product, name='delete-product'),
    path('products/batch/', create_batch_products, name='create-batch-products'),
    path('products/delete-all/', delete_all_products, name='delete-all-products'),
]
