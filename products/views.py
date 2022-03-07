from django.http  import JsonResponse
from django.views import View

from products.models import Product

class DetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            result = {
                'name'            : product.name,
                'stock'           : product.stock,
                'price'           : product.price if not product.stock == 0 else None,
                'discount_rate'   : float(product.productsdiscountrate_set.get(product_id=product.id).discount_rate.discount_rate)/100 if product.on_discount else None,
                'service_detail'  : product.service_detail.content,
                'thumbnail_image' : product.thumbnailimage.thumbnail_image_url,
                'detail_images'   : [detail_image.detail_image_url for detail_image in product.detailimage_set.all()],
                'product_options' : [product_option.time.name for product_option in product.producttime_set.filter(product_id=product.id)] if product.product_option else None,
                'reviews'         : [
                    {
                        'title'         : review.title,
                        'content'       : review.content,
                        'star_rating'   : review.star_rating,
                        'user'          : review.user.username,
                        'review_images' : [review_image.review_image_url for review_image in review.reviewimage_set.filter(review_id=review.id)]
                    }for review in product.review_set.filter(product_id=product.id)
                ] 
            }
            return JsonResponse({'result':result, 'message':'SUCCESS'}, status=200)      
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)