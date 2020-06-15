from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response

from .serializers import UserSerializer, UserSigninSerializer
from .authentication import token_expire_handler, expires_in


def index(request):
    return render(request, 'index.html')


@api_view(["POST"])
# here we specify permission by default we set IsAuthenticated
@permission_classes((AllowAny,))
def signin(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        email=signin_serializer.data['email'],
        password=signin_serializer.data['password']
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    # The implementation will be described further
    is_expired, token = token_expire_handler(token)
    user_serialized = UserSerializer(user)

    return Response({
        'email': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(["GET"])
def user_info(request):
    return Response({
        'email': request.user.email,
        'expires_in': expires_in(request.auth)
    }, status=HTTP_200_OK)