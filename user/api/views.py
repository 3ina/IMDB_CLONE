from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from user.api.serializers import RegisterSerializer

from user import models


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
