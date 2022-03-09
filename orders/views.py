import json

from django.http      import JsonResponse
from django.views     import View

from orders.models    import Cart
from products.models  import Product, ProductTime
from utils.decorators import signin_decorator


class CartView(View):
    @signin_decorator
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            
            quantity        = data['quantity']
            product_id      = data['product_id']
            product_time    = ProductTime.objects.get(product_id=product_id)
            
            cart, created = Cart.objects.get_or_create(
                user         = user,
                product_time = product_time,
                defaults     = {'quantity' : quantity},
            )
            
            if not created:
                cart.quantity += quantity
                cart.save()
                
                return JsonResponse({'message' : 'ADD_QUANTITY_TO_EXISTED_CART'}, status=200)
            
            return JsonResponse({'message' : 'CREATE_CART'}, status=201)
                
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except ProductTime.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT_OPTION'}, status=400)
        
    @signin_decorator
    def get(self, request):
        try:
            user    = request.user
            carts   = Cart.objects.filter(user=user)
        
            results = [
                {
                    'id'              : cart.id,
                    'name'            : cart.product_time.product.name,
                    'price'           : float(cart.product_time.product.price)*\
                                        (1-float(cart.product_time.product.productsdiscountrate_set.\
                                                get(product_id=cart.product_time.product.id).discount_rate.\
                                                discount_rate)/100) if cart.product_time.product.on_discount\
                                                else float(cart.product_time.product.price),
                    'time'            : cart.product_time.time.name,
                    'quantity'        : cart.quantity,
                    'total_price'     : float(cart.quantity)*\
                                        float(cart.product_time.product.price)*\
                                        (1-float(cart.product_time.product.productsdiscountrate_set.\
                                                get(product_id=cart.product_time.product.id).discount_rate.\
                                                discount_rate)/100) if cart.product_time.product.on_discount\
                                                else float(cart.quantity) * float(cart.product_time.product.price),
                    'thumbnail_image' : cart.product_time.product.thumbnailimage.thumbnail_image_url
                }
            for cart in carts]
        
            return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)
    
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)
        
    @signin_decorator
    def patch(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            
            quantity     = data['quantity']
            product_id   = data['product_id']
            product_time = ProductTime.objects.get(product_id=product_id)
            cart         = Cart.objects.filter(user=user, product_time=product_time)
            
            if not cart.exists():
                return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=400)
                
            cart.update(quantity = quantity)
            
            return JsonResponse({'message' : 'UPDATE_CART'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except ProductTime.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_TIME_NOT_EXIST'}, status=400)
        
    @signin_decorator
    def delete(self, request):
        try:
            user     = request.user
            carts_id = request.GET.getlist('cart_id')
            carts    = Cart.objects.filter(user=user, id__in=carts_id)
            
            carts.delete()
            
            return JsonResponse({'message' : 'DELETE_CART'}, status=204)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=400)
    
    