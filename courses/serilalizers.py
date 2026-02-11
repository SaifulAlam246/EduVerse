from rest_framework import serializers
from .models import Course, Purchase

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.ReadOnlyField(source='instructor.email')

    class Meta:
        model = Course
        fields = '__all__'