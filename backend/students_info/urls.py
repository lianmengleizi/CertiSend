from django.urls import path
from .views import UserInformationAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserInformationViewSet

router = DefaultRouter()
router.register(r'user-info', UserInformationViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 包含路由
]