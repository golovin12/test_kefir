from django.urls import path, re_path

from .views import UsersList, UserCurrent, UserUpdate, PrivateUsersListCreate, PrivateUserEdit, LogoutModel, LoginModel

app_name = 'api_users_control'

urlpatterns = [
    re_path(r'^login/$', LoginModel.as_view(), name='login'),
    re_path(r'^logout/$', LogoutModel.as_view(), name='logout'),
    path('users/', UsersList.as_view(), name='users_list'),
    path('users/current/', UserCurrent.as_view(), name='user_current'),
    path('users/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('private/users/', PrivateUsersListCreate.as_view(), name='private_users_list_create'),
    path('private/users/<int:pk>/', PrivateUserEdit.as_view(), name='private_user_edit'),
]
