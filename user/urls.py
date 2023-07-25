from rest_framework.routers import DefaultRouter
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views

# router = DefaultRouter()
# router.register('users', views.getusers, basename='user-list')


urlpatterns = [
    path('users/', views.UserView.as_view(), name='users'),
    # path('users/add/', views.UserCreate.as_view(), name='user-add'),
    # path('users/update<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    # path('users/delete<int:pk>', views.UserDeleteView.as_view(), name='user-delete'),
    path('users/list/', views.getusers, name="getusers"),
    path('users/deluser/',views.deluser,name="delsingleuser"),
    #path('account/logout/', views.LogoutView.as_view(), name='logout'),
    path('account/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/register/', views.Register, name="sign_up"),
    # path('users/', views.UserViewSet.as_view(), name='user_list')
]

