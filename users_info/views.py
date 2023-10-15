import math

from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404, ListAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel, CityModel
from .serializers import LoginSerializer, UserCurrentSerializer, UsersListSerializer, PrivateUsersListSerializer, \
    PrivateUsersRUDSerializer, CitySerializer

PAGE_SIZE = 2
MAX_PAGE_SIZE = 20


class UsersListPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'size'
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class PrivateUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.parser_context['kwargs'].get('pk') == request.user.id


class LoginModel(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = authenticate(request,
                                login=data['username'],
                                password=data['password'])
            if user is not None:
                login(request, user)
                return Response({'description': 'Successful Response'}, status=200)
            else:
                raise NotFound('Логин или пароль не действительны!')
        else:
            return Response(serializer.errors, status=400)


class LogoutModel(APIView):
    def get(self, request):
        logout(request)
        return Response({'description': 'Successful Response'}, status=200)


class UsersList(ListAPIView):
    users_list = ['id', 'login', 'first_name', 'last_name', 'email']
    permission_classes = [IsAuthenticated]
    pagination_class = UsersListPagination
    queryset = UserModel.objects.all().values(*users_list)
    serializer_class = UsersListSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = users_list
    search_fields = users_list

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            pagination_page = int(self._paginator.get_page_number(request, self._paginator))
            pagination_size = self._paginator.get_page_size(request)
            pagination_total = math.ceil(self._paginator.page.paginator.count / pagination_size)
            return Response({'data': serializer.data,
                             'meta': {
                                 'pagination': {
                                     'total': pagination_total,
                                     'page': pagination_page,
                                     'size': pagination_size
                                 }}})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data,
                         'meta': {
                             'pagination': {
                                 'total': 1,
                                 'page': 1,
                                 'size': PAGE_SIZE
                             }}})


class UserCurrent(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all().values(
        *['id', 'login', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin'])
    serializer_class = UserCurrentSerializer

    def get_object(self):
        obj = get_object_or_404(UserModel, login=self.request.user.login)
        return obj


class UserUpdate(UpdateModelMixin, GenericAPIView):
    queryset = UserModel.objects.all().values(
        *['id', 'login', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin'])
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = UserCurrentSerializer

    def get_object(self):
        obj = get_object_or_404(UserModel, login=self.request.user)
        return obj

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)


class PrivateUsersListCreate(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated, PrivateUserPermission]
    queryset = UserModel.objects.all().select_related('city')
    pagination_class = UsersListPagination
    serializer_class = PrivateUsersListSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'login', 'first_name', 'last_name', 'email', 'city__name']
    search_fields = ['id', 'login', 'first_name', 'last_name', 'email', 'city__name']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        cities = CityModel.objects.all().values_list()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            pagination_page = int(self._paginator.get_page_number(request, self._paginator))
            pagination_size = self._paginator.get_page_size(request)
            pagination_total = math.ceil(self._paginator.page.paginator.count / pagination_size)
            return Response({'data': serializer.data,
                             'meta': {
                                 'hint': {'city': cities},
                                 'pagination': {
                                     'total': pagination_total,
                                     'page': pagination_page,
                                     'size': pagination_size
                                 }}})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data,
                         'meta': {
                             'hint': {'city': cities},
                             'pagination': {
                                 'total': 1,
                                 'page': 1,
                                 'size': PAGE_SIZE
                             }}})

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PrivateUserEdit(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated, PrivateUserPermission]
    queryset = UserModel.objects.all().select_related('city')
    serializer_class = PrivateUsersRUDSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PrivateCitiesListCreate(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated, PrivateUserPermission]
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PrivateCityUpdateDelete(RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated, PrivateUserPermission]
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
