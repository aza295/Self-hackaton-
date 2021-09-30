from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import serializers
from registration.models import User
from registration.utils import send_activation_code


"""Создаем сериализатор для регистрации"""
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6,write_only=True)
    password_confirm = serializers.CharField(min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ('email','password','password_confirm')

    """Создаем проверку на введеные пароли"""
    def validate(self,validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email,password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Создаем сериализатор для логина"""
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label='password',
                                     style={'input-type':'password'},
                                     trim_whitespace=False
                                     )
    """Проверяем совпадают ли пароль и email"""
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request',),
                                email=email,
                                password=password)
            if not user:
                message = 'Невозможно залогиниться с предоставленными данными'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Должно включать  "email" и "пароль"'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs

"""Сериализатор который отправляет код для изменения пароля в случае если пользователь забыл пароль"""
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'password recovery',
            f'Your confirmation code: {user.activation_code}',
            'test2@gmail.com',
            [email]
        )

"""Сериализатор для смены пароля если забыл пароль"""
class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=8, required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User Not Registered')
        return email

    def validate_code(self, code):
            if not User.objects.filter(activation_code = code).exists():
                raise serializers.ValidationError('User Not Registered')
            return code

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Passwords Do Not Match')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()

"""Сериализатор для смены пароля"""
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Неверный Пароль')
        return old_pass

    def vaidate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return  attrs

    def  set_new_pass(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
