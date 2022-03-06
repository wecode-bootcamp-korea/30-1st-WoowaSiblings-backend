from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from products.models  import Product


class ProductListView(View):
    def get(self, request):
        try:
            limit    = int(request.GET.get('limit', 12))
            offset   = int(request.GET.get('offset', 0))
            category = request.GET.get('category', None)
            sorting  = request.GET.get('sort', '-created_at')
            
            q = Q()
            
            if category:
                q &= Q(category__name=category)

            products = Product.objects.filter(q).order_by(sorting)[offset:offset+limit]
            results  = []
            
            for product in products:
                on_discount   = product.on_discount
                discount_rate = float(product.productsdiscountrate_set.\
                                      get(product_id=product.id).\
                                      discount_rate.discount_rate)/100
                likes         = product.like_set.all().aggregate(Count('product_id'))\
                                ['product_id__count']
    
                results.append(
                    {
                        'id'              : product.id,
                        'name'            : product.name,
                        'price'           : float(product.price),
                        'discount_rate'   : discount_rate if on_discount else '',
                        'discount_price'  : float(product.price) * (1-discount_rate) if on_discount else '', 
                        'on_discount'     : on_discount,
                        'product_option'  : product.product_option,
                        'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                        'category'        : product.category.name,
                        'likes'           : likes
                    }
                )
                
            return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)