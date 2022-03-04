import json, re, bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View

from users.models        import User
from moonbanggu.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username     = data['username']
            password     = data['password']
            nickname     = data.get('nickname')
            email        = data.get('email')
            phone_number = data.get('phone_number', '')
            address      = data.get('address', '')
            zipcode      = data.get('zipcode', '')
            is_wecode    = data.get('is_wecode', True)
            point        = data.get('point', 100000)            
            batch_id     = data.get('batch_id', 1) 
            
            PASSWORD_REGEX  = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            EMAIL_REGEX     = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
            if email != None and not re.match(EMAIL_REGEX, email) :
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            
            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message':'USERNAME_ALREADY_EXISTS'}, status=400)
            
            if email != None and User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status=400)
            
            if nickname != None and User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'message':'NICKNAME_ALREADY_EXISTS'}, status=400)
            
            hashed_password         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            
            User.objects.create(
                username     = username,
                password     = decoded_hashed_password,
                nickname     = nickname,
                email        = email,
                phone_number = phone_number,
                address      = address,
                zipcode      = zipcode,
                is_wecode    = is_wecode,
                point        = point,
                batch_id     = batch_id    
            ) 
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)         
              
class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            password = data['password']
            username = data['username']
            user     = User.objects.get(username=username)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode(('utf-8'))):
                return JsonResponse({'message':'INVALID_USER'}, status=400)
                
            token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'message':'SUCCESS', 'ACCESS_TOKEN':token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)