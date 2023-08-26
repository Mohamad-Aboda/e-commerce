from django.urls import path, include 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apis import CreateUserAPIView, UserRetriveUpdateAPIView

app_name = 'accounts'
urlpatterns = [
    path('user/create/', CreateUserAPIView.as_view(), name='create-user'),
    path('user/update/', UserRetriveUpdateAPIView.as_view(), name='update-user'),


    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT token
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token

]
