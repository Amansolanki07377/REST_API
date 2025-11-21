from django.shortcuts import render

# Create your views here.from rest_framework import viewsets, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-joined_at')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], url_path='enroll', url_name='enroll')
    def enroll(self, request, pk=None):
        student = self.get_object()
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'detail': 'course_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'course not found'}, status=status.HTTP_404_NOT_FOUND)
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unenroll', url_name='unenroll')
    def unenroll(self, request, pk=None):
        student = self.get_object()
        course_id = request.data.get('course_id')
        try:
            enrollment = Enrollment.objects.get(student=student, course__id=course_id)
            enrollment.delete()
            return Response({'detail': 'unenrolled'}, status=status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response({'detail': 'enrollment not found'}, status=status.HTTP_404_NOT_FOUND)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enrollment.objects.all().order_by('-enrolled_on')
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

