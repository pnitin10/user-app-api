from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user import views


app_name = 'user'

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    # path('token/', views.CreateTokenView.as_view(), name='token'),
    path('', include(router.urls))
]
