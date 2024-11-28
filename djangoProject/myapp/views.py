from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal


def hello_world(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")

        required_fields = ['name', 'price', 'available']
        for field in required_fields:
            if field not in data:
                return HttpResponseBadRequest(f"Missing required field: {field}")

        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        try:
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Invalid data: {e.message_dict} ")
        except (TypeError, ValueError) as e:
            return HttpResponseBadRequest(f"Error in data format: {str(e)}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'available': product.available},
            status=201
        )
    else:
        return HttpResponseBadRequest("Invalid HTTP method for this endpoint.")


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound(f"Product with ID= {product_id} does not exist.")
    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'available': product.available
        })
    else:
        return HttpResponseBadRequest("Invalid HTTP method for this endpoint.")
