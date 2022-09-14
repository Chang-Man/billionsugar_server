from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from billionsugar_server.exceptions import FieldError, DuplicationError
import re

User = get_user_model()


def jwt_token_of(user):
    refresh = RefreshToken.for_user(user)
    jwt_token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    return jwt_token


def validated_password(password):
    if len(password) < 8 or len(password) > 20:
        return False
    match_num, match_alpha, match_special = re.search('[0-9]', password), re.search('[a-zA-z]', password), re.search('\W', password)
    if not match_num:
        if match_alpha and match_special:
            return True
    elif match_alpha or match_special:
        return True
    return False


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, max_length=255)
    nickname = serializers.CharField(required=True, max_length=30)
    phone = serializers.CharField(required=True, max_length=11)
    date_of_birth = serializers.DateField(required=True)

    def validate(self, data):
        password = data.get('password')
        if not validated_password(password):
            raise FieldError('영어, 숫자, 특문이 두종류 이상 조합된 8~20자의 비밀번호만 가능합니다.')

        username = data.get('username')
        email = data.get('email')
        nickname = data.get('nickname')
        phone = data.get('phone')

        queryset = User.objects.filter(username=username) | User.objects.filter(email=email) | User.objects.filter(
            nickname=nickname) | User.objects.filter(phone=phone)

        if queryset.filter(username=username).exists():
            raise DuplicationError('이미 존재하는 아이디입니다.')
        if queryset.filter(email=email).exists():
            raise DuplicationError('이미 존재하는 이메일입니다.')
        if queryset.filter(nickname=nickname).exists():
            raise DuplicationError('이미 존재하는 닉네임입니다.')
        if queryset.filter(phone=phone).exists():
            raise DuplicationError('이미 가입된 전화번호입니다.')

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        nickname = validated_data.get('nickname')
        phone = validated_data.get('phone')
        date_of_birth = validated_data.get('date_of_birth')
        user = User.objects.create_user(username=username, password=password, email=email, nickname=nickname, phone=phone, date_of_birth=date_of_birth)
        jwt_token = jwt_token_of(user)
        return user, jwt_token

