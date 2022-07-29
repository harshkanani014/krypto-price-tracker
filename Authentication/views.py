
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
import jwt, datetime
from django.http import JsonResponse
from django.contrib.auth.models import User


# Function to verify the accessToken
def verify_token(request):

    # Token can be passed through header or cookies
    try:
        if not (request.headers['Authorization'] == "null"):
            token = request.headers['Authorization']
    except:
        if not (request.COOKIES.get('token') == "null"):
            token = request.COOKIES.get('token')
    else:
        context = {
            "success":False,
            "message":"INVALID_TOKEN",
            }
        payload = JsonResponse(context)
    if not token:
        context = {
                "success":False,
                "message":"INVALID_TOKEN",
            }
        payload =  JsonResponse(context)

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except :
        context = {
                "success":False,
                "message":"INVALID_TOKEN",
            }
        payload =  JsonResponse(context)
    return payload
  

# Function For Parsing error from serializer
def get_error(serializerErr):

    err = ''
    for i in serializerErr:
        err = serializerErr[i][0]
        break    
    return err


# Task : Sign Up API for user where user can enter email and password
# API endpoint : /signup
# request : POST
class UserSignUpView(APIView):
    def post(self, request):
        context = request.data
        context._mutable = True
        context['username'] = request.data['email']
        context._mutable = False
        serializer = UserSerializer(data=context)

        # validate data using serializer
        if not serializer.is_valid():
            return Response({
            "success":False,
            "message":get_error(serializer.errors),
            })
        
        serializer.save()
        return Response({
            "success":True,
            "message":"User Sign Up successfully",
            "data":serializer.data
            })


# Task : Sign In and user validate for authentication. Access Token is generated
# API endpoint : /login
# request : POST
class UserLoginView(APIView):
    def post(self, request):

        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        # Check if user exists or not
        if user is None:
            context = {
                "success":False,
                "message":"User not found",
                "data":
                {
                    "user":email,
                }
            }
            return JsonResponse(context)

        # Validate password
        if not user.check_password(password):
            
            context = {
                "success":False,
                "message":"In-correct password",
                "data":
                {
                    "user":email,
                }
            }
            return JsonResponse(context)
        
        # Generate Payload with user id and token expire time
        payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45000),
                    'iat': datetime.datetime.utcnow()
                    }

        #generating token
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)

        response.data = {
                        "success":True,
                        "message":"User logged in successfully",
                        "data":
                            {
                            "accessToken":token,
                            "user":{
                                "id":user.id,
                                "name":user.email,
                                }
                            }
                        }
        
        return response


# Task : Logout current logged in user
# API endpoint : /logout
# request : POST
class UserLogoutView(APIView):

    def get(self, request):
        
        response = Response()
        response.delete_cookie('token') #delete the token
        
        response.data = {
            "error":"",
            'message': "success"
        }
        return response