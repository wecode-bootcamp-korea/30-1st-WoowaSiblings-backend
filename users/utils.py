import jwt

from django.http import JsonResponse

from moonbanggu.settings import SECRET_KEY, ALGORITHM
from users.models        import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(username=payload['username'])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        return func(self, request, *args, **kwargs)
       
    return wrapper