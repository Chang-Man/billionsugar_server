from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserCreateSerializer
from django.db import IntegrityError
from rest_framework import status, permissions
from rest_framework.response import Response


class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            raise status.HTTP_409_CONFLICT

        return Response({
            'user': user.username,
            'token': jwt_token
        }, status=status.HTTP_201_CREATED)

