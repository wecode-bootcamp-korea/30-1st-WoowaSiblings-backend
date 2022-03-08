from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from products.models  import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            result = {
                'name'            : product.name,
                'stock'           : product.stock,
                'price'           : product.price if not product.stock == 0 else '',
                'discount_rate'   : float(product.productsdiscountrate_set.\
                                    get(product_id=product.id).discount_rate.discount_rate)/100\
                                    if product.on_discount else '',
                'discount_price'  : (1-float(product.productsdiscountrate_set.\
                                    get(product_id=product.id).discount_rate.discount_rate)/100)*float(product.price)\
                                    if product.on_discount else '', 
                'service_detail'  : product.service_detail.content,
                'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                'detail_images'   : [detail_image.detail_image_url for detail_image in product.detailimage_set.all()],
                'product_options' : [product_option.time.name for product_option in product.producttime_set.all()]\
                                    if product.product_option else '',
                'reviews'         : [
                    {
                        'title'         : review.title,
                        'content'       : review.content,
                        'star_rating'   : review.star_rating,
                        'user'          : review.user.username,
                        'review_images' : [review_image.review_image_url for review_image in review.reviewimage_set.all()]
                    }for review in product.review_set.all()
                ] 
            }
            return JsonResponse({'result':result, 'message':'SUCCESS'}, status=200)      
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class ProductListView(View):
    def get(self, request):
        try:
            limit    = int(request.GET.get('limit', 12))
            offset   = int(request.GET.get('offset', 0))
            category = request.GET.get('category', None)
            sorting  = request.GET.get('order_by', 'new_products')
            
            sorting_dict = {
                'new_products'  : '-created_at',
                'old_products'  : 'created_at',
                'low_price'     : 'price',
                'high_price'    : '-price',
                'hot_products'  : '-likes'
            }
            
            q = Q()
            
            if category:
                q &= Q(category__name=category)

            products = Product.objects.filter(q).prefetch_related('like_set').\
                       annotate(likes=Count('like')).order_by(sorting_dict[sorting])\
                       [offset:offset+limit]
            
            results = [
                {
                    'id'              : product.id,
                    'name'            : product.name,
                    'price'           : float(product.price),
                    'discount_rate'   : float(product.productsdiscountrate_set.\
                                             get(product_id=product.id).\
                                             discount_rate.discount_rate)/100\
                                             if product.on_discount else '',
                    'discount_price'  : (1-float(product.productsdiscountrate_set.\
                                             get(product_id=product.id).discount_rate.\
                                             discount_rate)/100) * float(product.price)\
                                             if product.on_discount else '',
                    'on_discount'     : product.on_discount,
                    'product_options' : product.product_option,
                    'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                    'category'        : product.category.name,
                    'likes'           : product.like_set.count()
                }
            for product in products]
            
            return JsonResponse({'message' : 'SUCCESS', 'results' : results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)

