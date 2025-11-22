from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookViewSet, RegisterAPIView

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = router.urls + [
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', obtain_auth_token, name='api-login'),
]
