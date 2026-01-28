# Generated migration - Initial models

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_code', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='El código de empleado solo puede contener letras mayúsculas, números, guiones y guiones bajos.', regex='^[A-Z0-9_-]+$')], verbose_name='Código de Empleado')),
                ('full_name', models.CharField(max_length=200, verbose_name='Nombre Completo')),
                ('status', models.CharField(choices=[('active', 'Activo'), ('inactive', 'Inactivo')], default='active', max_length=10, verbose_name='Estado')),
                ('photo_ref', models.ImageField(upload_to='photos/', verbose_name='Foto de Referencia')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AttendanceEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('score', models.FloatField(help_text='Score de similitud facial (0.0 - 1.0)', verbose_name='Score de Similitud')),
                ('decision', models.BooleanField(help_text='True si el score >= threshold, False en caso contrario', verbose_name='Decisión')),
                ('provider_name', models.CharField(help_text='Nombre del proveedor de validación facial usado', max_length=100, verbose_name='Proveedor')),
                ('threshold_used', models.FloatField(help_text='Umbral de validación usado en este check-in', verbose_name='Umbral Aplicado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('employee', models.ForeignKey(on_delete=models.CASCADE, related_name='attendance_events', to='attendance.employee', verbose_name='Empleado')),
            ],
            options={
                'verbose_name': 'Evento de Asistencia',
                'verbose_name_plural': 'Eventos de Asistencia',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['employee_code'], name='attendance_e_employe_idx'),
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['status'], name='attendance_e_status_idx'),
        ),
        migrations.AddIndex(
            model_name='attendanceevent',
            index=models.Index(fields=['employee', '-timestamp'], name='attendance_a_employe_idx'),
        ),
        migrations.AddIndex(
            model_name='attendanceevent',
            index=models.Index(fields=['timestamp'], name='attendance_a_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='attendanceevent',
            index=models.Index(fields=['decision'], name='attendance_a_decisio_idx'),
        ),
    ]
