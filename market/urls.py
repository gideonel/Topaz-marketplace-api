from django.urls import path
from . import views

urlpatterns = [
    path('products/get/', views.get_products, name='get_products'),
    path('products/get/<int:id>/', views.get_product_by_id, name='get_product_by_id'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/batch-create/', views.create_batch_products, name='create_batch_products'),
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/delete-all/', views.delete_all_products, name='delete_all_products'),
]