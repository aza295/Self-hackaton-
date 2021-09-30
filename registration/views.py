from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from registration.models import User
from registration.serializers import LoginSerializer, ChangePasswordSerializer, \
    ForgotPasswordCompleteSerializer, ForgotPasswordSerializer, RegisterSerializer


class RegisterView(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Успешно Зарегистрирован",status=status.HTTP_201_CREATED)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class ActivateView(APIView):
     def get(self, request, activation_code ):
        user = get_user_model()
        user = get_object_or_404(User,activation_code=activation_code)
        user.is_active=True
        user.activation_code= ''
        user.save()
        return Response("Ваш аккаунт успешно активирован", status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из аккаунта',status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_code()
            return Response('Вам был выслан код восстановления ')
        return Response(serializer.errors, status=400)


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.set_new_password()
            return Response('Пароль успешно обновлен')
        return Response(serializer.errors, status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            serializer.set_new_pass()
            return Response('Вы успешно сменили пароль')
        return Response(serializer.errors, status=400)
