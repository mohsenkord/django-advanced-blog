from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer


class RegisterAPIView(generics.GenericAPIView):
    """View for registering new user"""
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            "user": {
                'id': user.id,
                'email': user.email,
            },
            "message": "User successfully registered",
        }
        return Response(data, status=status.HTTP_201_CREATED)
