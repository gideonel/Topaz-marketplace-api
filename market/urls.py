from django.urls import path
from market.views import (
    get_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    create_batch_products,
    delete_all_products,
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