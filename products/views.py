from django.http  import JsonResponse
from django.views import View

from products.models import *

class DetailView(View):
    def get(self, request):
        try:
            product = Product.objects.get(id=request.GET.get('product_id'))
            
            if product.stock == 0:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=200)
            
            if product.on_discount:
                discount_rate = float(product.productsdiscountrate_set.
                                       get(product_id=product.id).\
                                       discount_rate.discount_rate)/100
            
            if product.product_option:
                product_options = product.producttime_set.\
                                  filter(product_id=product.id)
                times=[]                  
                for product_option in product_options:
                    times.append(product_option.time.name)
            
            reviews = product.review_set.filter(product_id=product.id)
            reviews_li=[]
            for review in reviews:
                reviews_li.append(
                    {
                        'title'         : review.title,
                        'content'       : review.content,
                        'star_rating'   : review.star_rating,
                        'user'          : review.user.username,
                        'review_images' : [review_image.review_image_url for review_image in review.reviewimage_set.filter(review_id=review.id)]
                    }
                )
            
            result = {
                'name'            : product.name,
                'stock'           : product.stock,
                'price'           : product.price,
                'discount_rate'   : discount_rate if product.on_discount else None,
                'service_detail'  : product.service_detail.content,
                'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                'detail_images'   : [detail_image.detail_image_url for detail_image in product.detailimage_set.all()],
                'product_options' : times if product.product_option else None,
                'reviews'         : reviews_li if reviews_li else None,
            }

            return JsonResponse({'result':result}, status=200)                
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)