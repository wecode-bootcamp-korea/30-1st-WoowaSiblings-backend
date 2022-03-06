from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from products.models  import Product


class ProductListView(View):
    def get(self, request):
        try:
            limit    = int(request.GET.get('limit', 12))
            offset   = int(request.GET.get('offset', 0))
            category = request.GET.get('category', None)
            
            q = Q()
            
            if category:
                q &= Q(category__name=category)

            products = Product.objects.filter(q)[offset:offset+limit]
            results  = []
            
            for product in products:
                on_discount   = product.on_discount
                discount_rate = float(product.productsdiscountrate_set.\
                                      get(product_id=product.id).\
                                      discount_rate.discount_rate)/100
    
                results.append(
                    {
                        'id'              : product.id,
                        'name'            : product.name,
                        'price'           : float(product.price),
                        'discount_rate'   : discount_rate if on_discount else None,
                        'discount_price'  : float(product.price) * (1-discount_rate) if on_discount else None, 
                        'on_discount'     : on_discount,
                        'product_option'  : product.product_option,
                        'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                        'category'        : product.category.name,
                    }
                )
                
            return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)