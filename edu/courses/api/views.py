from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import detail_route

from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer

from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollView(APIView):
#     authentication_classes = (BaseAuthentication,)  # 认证
#     permission_classes = (IsAuthenticated,)  # 权限
#
#     def post(self, req, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(req.user)
#         return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['post'],
                  authentication_classes=[BaseAuthentication],
                  permission_classes=[IsAuthenticated])
    def enroll(self, req, *args, **kwargs):
        """
        自定义action: 学生选课
        """
        course = self.get_object()
        course.students.add(req.user)
        return Response({'enrolled': True})

    @detail_route(methods=['get'],
                  serializer_class=CourseWithContentsSerializer,
                  authentication_classes=[BaseAuthentication],
                  permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, req, *args, **kwargs):
        return self.retrieve(req, *args, **kwargs)
