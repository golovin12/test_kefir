from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('users_info.urls', namespace='api_users_control')),
    path('__debug__/', include('debug_toolbar.urls')),
]
