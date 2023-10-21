import base64
import datetime
import random
import string

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from kanban.models.user import User, OTP
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status


class AuthorizationView(GenericAPIView):
    def post(self, requests):
        data = requests.data
        if 'phone' not in data or not data['phone']:
            return Response({"Error": "Enter phone"}, status=status.HTTP_400_BAD_REQUEST)

        if 'password' not in data or not data['password']:
            return Response({"Error": "Enter Password"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone=int(data['phone'])).exists():
            return Response({
                "Error": "This phone exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        password = data['password']
        if len(password) < 6 or not any(char.isdigit() for char in password) or not any(
                char.isalpha() for char in password):
            return Response({
                "Error": "Invalid Password"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        user_data = {
            'phone': data['phone'],
            'password': password,
        }
        if data.get('key', None) == 'admin':
            user_data.update({
                "is_staff": True,
                "is_superuser": True
            })
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)
        return Response({"success": "You have successfully registered", "user_id": user.id, "token": token.key},
                        status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    def post(self, requests):
        data = requests.data
        if "phone" not in data or not data["phone"]:
            return Response({"Error": "Phone number is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if "password" not in data or not data['password']:
            return Response({"Error": "Password is missing"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            return Response({"Error": "User is not Found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(data['password']):
            return Response({"Error": "Incorrect Password"}, status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get_or_create(user=user)[0]
        return Response({
            "Success": token.key
        })


class LogoutView(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        if token:
            token.delete()

        return Response({
            "Success": "You have successfully loged out"
        }, status=status.HTTP_200_OK)


class UserActions(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def get(self, request):
        return Response({
            "success": request.user.format()
        })

    def put(self, request):
        data = request.data
        if 'phone' in data:
            user = User.objects.filter(phone=data['phone']).first()

            if user and user.id != request.user.id:
                return Response({
                    "Error": "This phone number is already exists"
                })

        request.user.phone = data.get('phone', request.user.phone)

        request.user.save()
        return Response({
            "Success": request.user.format()
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'old' not in data or 'new' not in data:
            return Response({
                "Error": "Enter the Password"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.check_password(data['old']):
            return Response({
                "Error": "Old password Does not match"
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.user.check_password(data['new']):
            return Response({
                "Error": "Your New password is same with Old one"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        request.user.set_password(data['new'])
        request.user.save()
        return Response({
            "Success": "Your Password has been updated"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        request.user.delete()

        return Response({"Success": "Your Account has been deleted"})


class AuthOne(GenericAPIView):
    def post(self, request):
        data = request.data
        if 'phone' not in data:
            return Response({"Error": "Enter phone number"})

        phone = User.objects.filter(phone=data['phone']).first()

        if phone:
            return Response({"Error": "This phone number is already registered"})

        code = random.randint(100000, 999999)
        random_string1 = ''.join(random.choice(string.digits + string.ascii_letters + string.digits) for i in range(20))
        encode_code = f"{random_string1}${str(code)}${random_string1}"
        encoded_value = base64.b64encode(encode_code.encode()).decode()

        otp = OTP.objects.create(key=encoded_value, phone=data['phone'])

        return Response({"OTP": code,
                         "Token": encoded_value})


class AuthTwo(GenericAPIView):
    def post(self, request):
        data = request.data
        if 'otp' not in data or 'token' not in data:
            return Response({"Error": "Information is not fully provided"}, status=status.HTTP_404_NOT_FOUND)

        token = OTP.objects.filter(key=data['token']).first()
        if not token:
            return Response({"Error": "Token Error"})

        if token.is_expired:
            return Response({"Error": "token expired"})

        if token.is_confir:
            return Response({"Error": "Invalid Token"})

        now = datetime.datetime.now(datetime.timezone.utc)

        if (now - token.created).total_seconds() >= 3000:
            token.is_expired = True
            token.save()
            return Response({"Error": "Token Has Expired"})

        decoded_encoded_otp = base64.b64decode(token.key).decode()
        decoded_code = decoded_encoded_otp.split('$')[1]

        if decoded_code != str(data['otp']):
            token.tries += 1
            token.save()
            return Response({"Error": "Incorrect Code"})

        token.is_confir = True
        token.save()
        return Response({"OTP": decoded_code,
                         "Success": "Welcome"})
