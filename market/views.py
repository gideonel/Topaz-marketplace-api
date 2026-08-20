import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import Product

from rest_framework.decorators import api_view
from rest_framework.response import Response



def parse_price(value):
    try:
        price = Decimal(str(value))
        if not price.is_finite() or price < 0:
            raise ValueError
        return Product._meta.get_field('price').clean(price, None)
    except (InvalidOperation, TypeError, ValueError, ValidationError):
        raise ValueError('Price must be a valid non-negative amount with at most two decimal places.')



def product_to_dict(product, request=None):

    """Convert a Product instance to a dictionary representation, including the image_url URL if available."""
    image_url = ''
    if product.image:
        if request:
            image_url = request.build_absolute_uri(product.image_url.url)
        else:
            image_url = product.image_url.url
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock,
        'category': product.category,
        'image': image_url,
    }

 #this is the view for the get_products endpoint : it feches all products from the database and returns them as a JSON response.
 #  It uses the product_to_dict function to convert each Product instance into a dictionary representation, including the image_url if available. 
 # If an error occurs during the process, it returns a JSON response with an error message and a 500 status code.


@csrf_exempt
@api_view(["GET"])
def get_products(request):
    """Retrieve all products and return them as a JSON response."""
    try:
        products = Product.objects.all()
        products_list = [product_to_dict(product, request) for product in products]
        return JsonResponse(products_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# this is to get product by id

@csrf_exempt
@api_view(["GET"])
def get_product_by_id(request, id):
    """Retrieve a product by ID and return it as a JSON response."""
    try:
        product = Product.objects.get(pk=id)
        return Response(product_to_dict(product, request))
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@api_view(["POST"])
def create_product(request):
    """Create a new product from the provided JSON data."""
    try:
        # Handle both JSON and multipart/form-data requests

        if request.content_type  and 'multipart' in request.content_type:
            data = request.POST
            image = request.FILES.get('image')
        else:
            data = json.loads(request.body)
            image = None

        # Extract product data from the request
        name = data.get('name').strip()
        description = data.get('description', '').strip()
        price = data.get('price', '').strip()
        stock = data.get('stock', '0').strip()
        category = data.get('category', '').strip()

        # Validate required fields
        if not name or not price or not stock:
            return JsonResponse({'error': 'Name, price, and stock are required fields.'}, status=400)

        try:
            price = parse_price(price)
            stock = int(stock)
        except (ValueError, TypeError):
            return JsonResponse(
                {'error': 'Price must be a number and stock must be an integer.'},
                  status=400
                )

        # Create the product

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image
        )

        if image:
            product.image = image

        product.save()

        return JsonResponse(
            {'status': 'success', 'product': product_to_dict(product, request)}, status=201)

    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid data provided.'},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=400
        )


@csrf_exempt
@api_view(["PUT"])
def update_product(request,id):

    """Update an existing product in the database based on the provided ID and JSON data."""

    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Product not found.'},
            status=404
        )

    try:
        data = json.loads(request.body)

        # Update product fields if they are provided in the request

        if 'name' in data and data['name'].strip():
            product.name = data['name'].strip()
        if 'description' in data:
            product.description = data['description'].strip() if data['description'] else ''
        if 'price' in data:
            product.price = parse_price(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        if 'category' in data:
            product.category = data['category'].strip() if data['category'] else ''
        if 'image' in data and data['image'].strip():
            product.image = data['image']

        product.save()

        return JsonResponse(
            {'status': 'success', 'product': product_to_dict(product, request)},
            status=200
        )

    except ValueError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid data provided.'},
            status=400
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON.'},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=500
        )


@csrf_exempt
@api_view(["DELETE"])
def delete_product(request, id):
    """Delete a product by ID and return a JSON response indicating success or failure."""

    try:
        product = Product.objects.get(pk=id)
        product.delete()
        return JsonResponse({'status': 'success', 'message': f'Product with ID {id} deleted successfully.'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'Product with ID {id} not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




#create batch products endpoint
@csrf_exempt
@api_view(["POST"])
def create_batch_products(request):
    """Create multiple products from the provided JSON data."""
    try:
        data = json.loads(request.body)
        if not isinstance(data, list):
            return JsonResponse({'error': 'Expected a list of products.'}, status=400)

        created_products = []
        for product_data in data:
            name = product_data.get('name', '').strip()
            description = product_data.get('description', '').strip()
            price = product_data.get('price', '').strip()
            stock = product_data.get('stock', '0').strip()
            category = product_data.get('category', '').strip()

            # Validate required fields
            if not name or not price or not stock:
                return JsonResponse({'error': 'Name, price, and stock are required fields for each product.'}, status=400)

            try:
                price = parse_price(price)
                stock = int(stock)
            except (ValueError, TypeError):
                return JsonResponse(
                    {'error': 'Price must be a number and stock must be an integer for each product.'},
                    status=400
                )

            # Create the product
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category=category
            )
            product.save()
            created_products.append(product_to_dict(product, request))

        return JsonResponse({'status': 'success', 'products': created_products}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


# Delete all products endpoint
@csrf_exempt
@api_view(["DELETE"])
def delete_all_products(request):
    """Delete all products from the database and return a JSON response indicating success or failure."""
    try:
        count, _ = Product.objects.all().delete()
        return JsonResponse(
            {'status': 'success', 
             'message': f'All products deleted successfully. Total deleted: {count}.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
