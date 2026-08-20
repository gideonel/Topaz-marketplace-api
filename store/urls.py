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
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from market.views import get_products, get_product_by_id, create_product, update_product, delete_product

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
    path('admin/', admin.site.urls),
    path('market/api/', include('market.urls')),
    path('market/api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('market/api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
