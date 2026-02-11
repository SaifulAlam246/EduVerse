from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from courses.views import CourseViewSet, AdminDashboardStats

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin-stats/', AdminDashboardStats.as_view(), name='admin-stats'),
]