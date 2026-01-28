# Arquitectura del Sistema

## Visión General

El sistema está diseñado siguiendo principios de **Arquitectura Limpia** y **Separación de Responsabilidades**, organizado en capas bien definidas que facilitan el mantenimiento, testing y escalabilidad.

## Capas de Arquitectura

### 1. API Layer (Capa de Presentación)

**Ubicación**: `attendance/views.py`, `attendance/serializers.py`

**Responsabilidades**:
- Recibir y validar requests HTTP
- Serializar/deserializar datos
- Manejar respuestas HTTP
- **NO contiene lógica de negocio**

**Componentes**:
- `EmployeeViewSet`: CRUD de empleados
- `CheckInView`: Endpoint de check-in
- `AttendanceEventViewSet`: Consulta de eventos
- Serializers para validación y transformación de datos

### 2. Services Layer (Capa de Lógica de Negocio)

**Ubicación**: `attendance/services/`

**Responsabilidades**:
- Implementar casos de uso específicos
- Orquestar operaciones entre repositorios y providers
- Aplicar reglas de negocio
- Manejar transacciones lógicas

**Servicios**:
- `CreateEmployeeService`: Crear empleado con validaciones
- `UpdateEmployeeService`: Actualizar empleado
- `DeleteEmployeeService`: Eliminar empleado
- `CheckInEmployeeService`: Proceso completo de check-in

**Principios**:
- Cada servicio maneja un caso de uso específico
- Los servicios son independientes y testables
- No dependen directamente de Django (solo de modelos/repositorios)

### 3. Repositories Layer (Capa de Acceso a Datos)

**Ubicación**: `attendance/repositories/`

**Responsabilidades**:
- Abstraer el acceso a la base de datos
- Proporcionar métodos de alto nivel para operaciones CRUD
- Centralizar queries complejas
- Facilitar testing con mocks

**Repositorios**:
- `EmployeeRepository`: Operaciones sobre Employee
- `AttendanceRepository`: Operaciones sobre AttendanceEvent

**Ventajas**:
- Desacoplamiento de Django ORM
- Fácil migración a otro ORM o DB
- Testing simplificado con mocks

### 4. Providers Layer (Capa de Integración Externa)

**Ubicación**: `attendance/providers/`

**Responsabilidades**:
- Abstraer integraciones con servicios externos
- Proporcionar interfaz común para diferentes proveedores
- Facilitar el cambio de proveedor sin afectar otras capas

**Componentes**:
- `FaceVerificationProvider`: Interfaz abstracta
- `DummyProvider`: Implementación simulada
- `factory.py`: Factory para obtener el provider configurado

**Diseño**:
- Patrón Strategy para diferentes proveedores
- Fácil extensión para nuevos proveedores (AWS Rekognition, Azure Face API, etc.)

### 5. Core Layer (Capa de Configuración)

**Ubicación**: `core/`, `attendance/models.py`

**Responsabilidades**:
- Configuración de Django
- Modelos de datos
- Settings y variables de entorno
- Logging

## Flujo de Datos

### Flujo de Check-in

```
1. Frontend (React)
   └─> Captura imagen con getUserMedia
   └─> Convierte a base64
   └─> POST /api/check-in/

2. API Layer (CheckInView)
   └─> Valida request con CheckInSerializer
   └─> Llama a CheckInEmployeeService

3. Service Layer (CheckInEmployeeService)
   └─> Busca empleado (EmployeeRepository)
   └─> Valida que esté activo
   └─> Procesa imagen capturada (base64 -> bytes)
   └─> Lee imagen de referencia
   └─> Llama a FaceVerificationProvider.verify()
   └─> Aplica threshold
   └─> Guarda evento (AttendanceRepository)
   └─> Retorna resultado

4. Provider Layer (DummyProvider)
   └─> Calcula score determinístico
   └─> Retorna {score, match, provider}

5. Response
   └─> Serializa resultado
   └─> Retorna JSON al frontend
```

## Decisiones de Diseño

### 1. Separación por Capas

**Razón**: Facilita el mantenimiento, testing y escalabilidad. Cada capa tiene responsabilidades claras.

**Beneficios**:
- Cambios en una capa no afectan otras
- Testing independiente por capa
- Fácil reemplazo de componentes

### 2. Repositorios en lugar de acceso directo a ORM

**Razón**: Abstrae el acceso a datos, facilitando:
- Testing con mocks
- Cambio de ORM/DB sin afectar servicios
- Centralización de queries complejas

### 3. Servicios para Lógica de Negocio

**Razón**: Evita "fat views" y mantiene la lógica de negocio separada de la presentación.

**Beneficios**:
- Views delgadas y enfocadas en HTTP
- Servicios reutilizables
- Lógica de negocio testeable

### 4. Provider Pattern para Face API

**Razón**: Permite cambiar el proveedor de validación facial sin modificar el resto del código.

**Implementación**:
- Interfaz abstracta `FaceVerificationProvider`
- Factory para obtener el provider configurado
- Fácil extensión para nuevos proveedores

### 5. No Guardar Foto de Check-in

**Razón**: Requisito explícito del sistema. Solo se procesa en memoria y se guarda el evento con metadata.

**Implementación**:
- Imagen capturada se procesa en memoria
- Solo se guarda `photo_ref` del empleado
- Evento guarda score, decision, timestamp, pero no la imagen

## Testing Strategy

### Unit Tests
- **Providers**: Verificar lógica de cálculo de score
- **Services**: Validar casos de uso con mocks
- **Repositories**: Verificar operaciones CRUD

### Integration Tests
- **API Endpoints**: Flujo completo HTTP
- **Check-in completo**: Desde request hasta guardado de evento
- **CRUD completo**: Crear, leer, actualizar, eliminar

### Mocking Strategy
- Repositorios mockeados en tests de servicios
- Providers mockeados en tests de servicios
- Base de datos de test para integration tests

## Escalabilidad

### Horizontal Scaling
- Backend stateless (sin sesiones)
- Base de datos PostgreSQL escalable
- Frontend puede servir desde CDN

### Vertical Scaling
- Servicios independientes permiten optimización individual
- Repositorios pueden optimizarse con índices
- Providers pueden cachear resultados

### Extensibilidad

**Nuevos Proveedores de Face API**:
1. Implementar `FaceVerificationProvider`
2. Registrar en factory
3. Configurar en settings

**Nuevos Casos de Uso**:
1. Crear nuevo servicio en `services/`
2. Crear endpoint en `views.py`
3. Agregar serializer si es necesario

**Nuevas Funcionalidades**:
- La arquitectura por capas facilita agregar nuevas features
- Cada capa puede extenderse independientemente

## Seguridad

### Validación de Inputs
- Serializers validan todos los inputs
- Servicios validan reglas de negocio
- Repositorios validan integridad de datos

### Manejo de Errores
- Errores específicos por capa
- Logging de errores para debugging
- Respuestas HTTP apropiadas

### Consideraciones Futuras
- Autenticación (actualmente endpoints abiertos)
- Rate limiting
- Validación de imágenes más robusta
- Encriptación de datos sensibles

## Monitoreo y Logging

- Logging configurado en `core/settings.py`
- Logs por módulo (`attendance`, `django`)
- Niveles configurables (DEBUG, INFO, ERROR)
- Preparado para integración con sistemas de monitoreo
