import json

from django.http  import JsonResponse
from django.views import View

from products.models  import Product
from utils.decorators import signin_decorator

class LikeView(View):
    @signin_decorator
    def post(self, request):
        
        data          = json.loads(request.body)
        product       = Product.objects.get(id=data['product_id'])
        user          = request.user
        obj, _created = product.like_set.get_or_create(user_id=user.id)
        
        if not _created:
            obj.delete()
            return JsonResponse({'message':'UNLIKED'}, status=200)
               
        return JsonResponse({'message':'LIKED'}, status=200)