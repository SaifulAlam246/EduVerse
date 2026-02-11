from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Course, Purchase
from .serilalizers import CourseSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class IsInstructorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses.
    
    list: Return a list of all available courses (supports department filtering).
    create: Create a new course. The authenticated user is automatically set as the instructor.
    retrieve: Return the details of a specific course.
    update: Fully update a course (Restricted to the course instructor).
    partial_update: Partially update course details (Restricted to the course instructor).
    destroy: Delete a course (Restricted to the course instructor).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ['department']

    
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def get_queryset(self):
        if getattr(self,'swagger_fake_view', False):
            return Course.objects.none()
        
        if self.action in ['update', 'partial_update', 'destroy']:
            return Course.objects.filter(instructor=self.request.user)
        return Course.objects.all()
    

class AdminDashboardStats(APIView):
    """
    Retrieve analytical statistics for the Admin Dashboard.
    
    GET:
    Returns a summary of platform performance including:
    - top_5_students: Students with the highest number of purchases.
    - mostly_purchased_courses: Most popular courses based on sales volume.
    - current_month_sales: Total revenue generated in the current calendar month.
    - previous_month_sales: Total revenue generated in the previous calendar month.
    - last_week_purchases: Count of individual purchases made in the last 7 days.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
        last_month = (start_of_month - timedelta(days=1)).replace(day=1)

        context = {
            "top_5_students": Purchase.objects.values('student__username').annotate(count=Count('id')).order_by('-count')[:5],
            "mostly_purchased_courses": Purchase.objects.values('course__title').annotate(count=Count('id')).order_by('-count')[:5],
            "current_month_sales": Purchase.objects.filter(purchased_at__gte=start_of_month).aggregate(Sum('amount')),
            "previous_month_sales": Purchase.objects.filter(purchased_at__range=[last_month, start_of_month]).aggregate(Sum('amount')),
            "last_week_purchases": Purchase.objects.filter(purchased_at__gte=now - timedelta(days=7)).count()
        }
        return Response(context, status=status.HTTP_200_OK)