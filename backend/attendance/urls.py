"""
URLs for attendance API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'attendance-events', views.AttendanceEventViewSet, basename='attendance-event')

urlpatterns = [
    path('', include(router.urls)),
    path('check-in/', views.CheckInView.as_view(), name='check-in'),
]
