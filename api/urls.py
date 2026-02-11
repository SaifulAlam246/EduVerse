from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, AdminDashboardStats

router = DefaultRouter()
router.include_format_suffixes = False
router.register('courses', CourseViewSet, basename='course')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin-stats/', AdminDashboardStats.as_view(), name='admin-stats'),
     path('', include(router.urls)),
]