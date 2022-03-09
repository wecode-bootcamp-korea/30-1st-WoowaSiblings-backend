import json
import datetime

from django.http import JsonResponse
from django.views import View

from products.models  import ProductTime
from reviews.models   import Review, ReviewImage
from utils.decorators import signin_decorator

class ReviewView(View):
    @signin_decorator
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            user = request.user
            
            if Review.objects.filter(user_id=user.id, product_id=product_id).exists():
                return JsonResponse({'message':'REVIEW_ALREADY_EXISTS'}, status=403)
            
            try:
                orders           = user.order_set.filter(order_status_code_id=1,\
                                   updated_at__range=[datetime.datetime.today()-datetime.timedelta(days=14), datetime.datetime.today()])
                review_available = False
                for order in orders:
                    order_items = order.orderitem_set.filter(order_item_status_code=1)
                    if order_items.exists():
                        for order_item in order_items:
                            order_item_id = order_item.product_time.product_id
                            if order_item_id == product_id:
                                review_available = True
                                break
                            else:
                                continue
                        break
                    else:
                        continue
                
                if not review_available:
                    return JsonResponse({'message':'NO_REVIEW_AVAILABLE'}, status=403)
                
            except IndexError:
                return JsonResponse({'message':'NO_REVIEW_AVAILABLE'}, status=403)
                    
            except ProductTime.DoesNotExist:
                return JsonResponse({'message':'NO_REVIEW_AVAILABLE'}, status=403)
                
            review = Review.objects.create(
                title       = data['title'],
                content     = data['content'],
                star_rating = data['star_rating'],
                user        = user,
                product_id  = product_id
            )
            
            if data['review_image_url']:
                ReviewImage.objects.create(
                    review_image_url = data['review_image_url'],
                    review           = review
                )
            
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except:
            pass
        
        
        
        