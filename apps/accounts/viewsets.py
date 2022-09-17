from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Account
from .serializers import (
    AccountRegisterSerializer,
    AccountSerializer,
    CheckEmailSerializer,
    UserLoginSerializer,
    UserResetPasswordCodeSerializer,
    UserResetPasswordSerializer,
    UserResetPasswordSetPasswordSerializer
)
from apps.utils.permissions import IsAccount, IsRegisterEnabled
from apps.utils.viewsets import OwnerModelViewSet


class AccountRegisterViewSet(viewsets.GenericViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(deleted=False)

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=CheckEmailSerializer)
    def check_email(self, request):
        """User check email."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny, IsRegisterEnabled],
            serializer_class=AccountRegisterSerializer)
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class AccountAuthViewSet(viewsets.GenericViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(deleted=False)
    permission_classes = [
        IsAuthenticated,
        IsAccount,
    ]

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserLoginSerializer)
    def login(self, request):
        """User sign in."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        return Response({
            'user': user,
            'token': token
        })

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserResetPasswordSerializer)
    def send_reset_code(self, request):
        username = request.data.get('username')
        user = get_object_or_404(Account, username=username)
        user.generate_reset_password_code()
        return Response({
            "success": True
        })

    @action(detail=False,
            permission_classes=[AllowAny],
            methods=['POST'],
            serializer_class=UserResetPasswordCodeSerializer)
    def check_reset_password_code(self, request):
        username = request.data.get('username')
        reset_password_code = request.data.get('code')
        get_object_or_404(Account, username=username, reset_password_code=reset_password_code)
        return Response({
            "success": True
        })

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=UserResetPasswordSetPasswordSerializer)
    def set_new_password(self, request):
        username = request.data.get('username')
        code = request.data.get('code')
        password = request.data.get('password')
        user = get_object_or_404(Account, username=username, reset_password_code=code)
        user.reset_password(password)
        return Response({
            "success": True
        })

    @action(detail=False, methods=['GET'])
    def detail_user(self, request):
        serializer = self.serializer_class(request.user.account)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_user(self, request):
        serializer = self.serializer_class(request.user.account, request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class AccountOwnerViewSet(OwnerModelViewSet):
    serializer_class = AccountRegisterSerializer
    queryset = Account.objects.filter(deleted=False)
    search_fields = ('username', 'first_name', 'last_name',)

    @action(detail=True, methods=['DELETE'], serializer_class=None)
    def delete(self, request, uuid=None):
        result = self.get_object().logical_erase()
        return Response(result)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def disable(self, request, uuid=None):
        result = self.get_object().disable()
        return Response(result)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def enable(self, request, uuid=None):
        result = self.get_object().enable()
        return Response(result)

