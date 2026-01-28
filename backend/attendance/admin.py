"""
Admin configuration for attendance models.
"""
from django.contrib import admin
from attendance.models import Employee, AttendanceEvent


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'full_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['employee_code', 'full_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AttendanceEvent)
class AttendanceEventAdmin(admin.ModelAdmin):
    list_display = ['employee', 'timestamp', 'score', 'decision', 'provider_name']
    list_filter = ['decision', 'provider_name', 'timestamp']
    search_fields = ['employee__employee_code', 'employee__full_name']
    readonly_fields = ['created_at']
    date_hierarchy = 'timestamp'
