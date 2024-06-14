from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from user.api.serializers import RegisterSerializer

from user import models

@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response(description="Logout successful"),
        401: openapi.Response(description="Unauthorized")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request : HttpRequest):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)




@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="Registration Successful",
            examples={
                "application/json": {
                    "response": "Registration Successful!",
                    "username": "user",
                    "email": "user@example.com",
                    "token": {
                        "refresh": "refresh_token_example",
                        "access": "access_token_example"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "username": ["This field is required."],
                    "email": ["This field is required."],
                    "password": ["This field is required."]
                }
            }
        )
    }
)
@api_view(['POST'])
def registration_view(request):
    if request.method == "POST":
        data = {}
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)

            data["token"] = {
                'refresh': str(refresh),
                "access": str(refresh.access_token),
            }
        else:
            data = serializer.errors
            return Response(data,status.HTTP_400_BAD_REQUEST)

        return Response(data,status.HTTP_201_CREATED)
