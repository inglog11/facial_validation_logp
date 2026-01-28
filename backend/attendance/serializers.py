"""
Serializers for attendance API.
"""
from rest_framework import serializers
from attendance.models import Employee, AttendanceEvent
from attendance.services import (
    CreateEmployeeService,
    UpdateEmployeeService,
    DeleteEmployeeService,
)


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer para Employee."""
    
    photo_ref_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_code',
            'full_name',
            'status',
            'photo_ref',
            'photo_ref_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_photo_ref_url(self, obj):
        """Obtener URL completa de la foto de referencia."""
        if obj.photo_ref:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo_ref.url)
            return obj.photo_ref.url
        return None


class EmployeeCreateSerializer(serializers.Serializer):
    """Serializer para crear empleado."""
    
    employee_code = serializers.CharField(max_length=50)
    full_name = serializers.CharField(max_length=200)
    status = serializers.ChoiceField(choices=['active', 'inactive'], default='active')
    photo_ref = serializers.ImageField()
    
    def create(self, validated_data):
        """Crear empleado usando el servicio."""
        service = CreateEmployeeService()
        return service.execute(**validated_data)


class EmployeeUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar empleado."""
    
    full_name = serializers.CharField(max_length=200, required=False)
    status = serializers.ChoiceField(
        choices=['active', 'inactive'],
        required=False
    )
    photo_ref = serializers.ImageField(required=False)
    
    def update(self, instance, validated_data):
        """Actualizar empleado usando el servicio."""
        service = UpdateEmployeeService()
        return service.execute(
            employee_id=instance.id,
            **validated_data
        )


class CheckInSerializer(serializers.Serializer):
    """Serializer para check-in."""
    
    employee_code = serializers.CharField(max_length=50)
    capture_image = serializers.CharField(
        help_text='Imagen capturada en base64 (data:image/...;base64,...)'
    )
    
    def validate_capture_image(self, value):
        """Validar formato de imagen."""
        if not value.startswith('data:image/'):
            raise serializers.ValidationError(
                "La imagen debe estar en formato base64 con prefijo data:image/"
            )
        return value


class CheckInResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de check-in."""
    
    decision = serializers.BooleanField()
    score = serializers.FloatField()
    threshold_used = serializers.FloatField()
    employee_code = serializers.CharField()
    timestamp = serializers.DateTimeField()


class AttendanceEventSerializer(serializers.ModelSerializer):
    """Serializer para eventos de asistencia."""
    
    employee_code = serializers.CharField(source='employee.employee_code', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    
    class Meta:
        model = AttendanceEvent
        fields = [
            'id',
            'employee_code',
            'employee_name',
            'timestamp',
            'score',
            'decision',
            'provider_name',
            'threshold_used',
            'created_at',
        ]
        read_only_fields = '__all__'
