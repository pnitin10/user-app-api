import json
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse

from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.settings import api_settings

from user.serializers import UserSerializer
from core import models


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """To not perform the csrf check previously happening."""

    def enforce_csrf(self, request):
        return


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for user."""
#
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user."""
        return self.request.user


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles."""

    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (authentication.SessionAuthentication,)


class LoginAPIView(APIView):
    """Login API."""

    serializer_class = UserSerializer

    def post(self, request, format=None):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return JsonResponse({
                "errors": {
                    "__all__": "Please enter both username and password"
                }
            }, status=400)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'message': 'Login Successfully', 'username': user.username}
            return Response(data, status=status.HTTP_200_OK)
        return JsonResponse(
            {"detail": "Invalid credentials"},
            status=400,
        )


class LogoutAPIView(APIView):
    """Logout API."""

    def get(self, request, format=None):
        """
        Removes the authenticated user's ID from the request and flushes
        their session data.
        """
        logout(request)
        message = {'message': 'You have successfully logged out!'}
        return Response(message, status=status.HTTP_200_OK)
