# Sistema de Registro de Entrada con Validación Facial

## Descripción

Sistema para registrar la entrada de empleados mediante validación facial, comparando una imagen capturada en el ingreso (desde cámara del navegador) contra una imagen de referencia (foto del carnet) previamente registrada.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                      │
│  ┌──────────────┐  ┌──────────────────────────────────┐    │
│  │  CRUD View   │  │      Check-in View                │    │
│  │              │  │  ┌────────────────────────────┐  │    │
│  │  - List      │  │  │  Camera Capture            │  │    │
│  │  - Create    │  │  │  (getUserMedia)            │  │    │
│  │  - Edit      │  │  └────────────────────────────┘  │    │
│  │  - Delete    │  │  ┌────────────────────────────┐  │    │
│  └──────────────┘  │  │  Send to API               │  │    │
│                    │  │  Display Result             │  │    │
│                    │  └────────────────────────────┘  │    │
│                    └──────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Django + DRF)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API LAYER (Views/Serializers)            │  │
│  │  - EmployeeViewSet (CRUD)                             │  │
│  │  - CheckInView (POST /check-in/)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SERVICES LAYER                            │  │
│  │  - CreateEmployeeService                              │  │
│  │  - UpdateEmployeeService                              │  │
│  │  - DeleteEmployeeService                              │  │
│  │  - CheckInEmployeeService                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           REPOSITORIES LAYER                          │  │
│  │  - EmployeeRepository                                 │  │
│  │  - AttendanceRepository                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           PROVIDERS LAYER                             │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  FaceVerificationProvider (Interface)           │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                    ▲                                  │  │
│  │                    │                                  │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  DummyProvider (Simulación)                     │  │  │
│  │  │  - verify() -> {score, match, provider}         │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              CORE LAYER                                │  │
│  │  - Models (Employee, AttendanceEvent)                 │  │
│  │  - Settings (threshold, media config)                 │  │
│  │  - Logging                                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   (Docker)      │
                    └─────────────────┘
```

## Modelo de Datos

### Employee
- `id`: PK autoincremental
- `employee_code`: Código único del empleado (único)
- `full_name`: Nombre completo
- `status`: Estado (active/inactive)
- `photo_ref`: Ruta a la imagen de referencia (carnet)
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de actualización

### AttendanceEvent
- `id`: PK autoincremental
- `employee`: FK a Employee
- `timestamp`: Timestamp del check-in
- `score`: Score de similitud (0.0 - 1.0)
- `decision`: Boolean (match/no match)
- `provider_name`: Nombre del proveedor usado
- `threshold_used`: Umbral aplicado
- `created_at`: Timestamp de creación

## Endpoints API

### CRUD Empleados

#### Listar empleados
```
GET /api/employees/
Response: 200 OK
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee_code": "EMP001",
      "full_name": "Juan Pérez",
      "status": "active",
      "photo_ref": "/media/photos/EMP001.jpg",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

#### Crear empleado
```
POST /api/employees/
Content-Type: multipart/form-data
{
  "employee_code": "EMP001",
  "full_name": "Juan Pérez",
  "status": "active",
  "photo_ref": <file>
}
Response: 201 Created
{
  "id": 1,
  "employee_code": "EMP001",
  "full_name": "Juan Pérez",
  "status": "active",
  "photo_ref": "/media/photos/EMP001.jpg",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Obtener empleado
```
GET /api/employees/{id}/
Response: 200 OK
{
  "id": 1,
  "employee_code": "EMP001",
  "full_name": "Juan Pérez",
  "status": "active",
  "photo_ref": "/media/photos/EMP001.jpg",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Actualizar empleado
```
PUT /api/employees/{id}/
Content-Type: multipart/form-data
{
  "employee_code": "EMP001",
  "full_name": "Juan Pérez García",
  "status": "active",
  "photo_ref": <file> (opcional)
}
Response: 200 OK
{
  "id": 1,
  "employee_code": "EMP001",
  "full_name": "Juan Pérez García",
  "status": "active",
  "photo_ref": "/media/photos/EMP001.jpg",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Eliminar empleado
```
DELETE /api/employees/{id}/
Response: 204 No Content
```

### Check-in

#### Registrar entrada
```
POST /api/check-in/
Content-Type: application/json
{
  "employee_code": "EMP001",
  "capture_image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
Response: 200 OK
{
  "decision": true,
  "score": 0.85,
  "threshold_used": 0.80,
  "employee_code": "EMP001",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

## Requisitos Previos

- Docker
- Docker Compose

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd Prueba_Tecnica_CS
```

### 2. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=attendance_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Face Verification
FACE_VERIFICATION_THRESHOLD=0.80

# Media Storage (local por defecto, preparado para S3/MinIO)
MEDIA_ROOT=/app/media
```

### 3. Construir y ejecutar con Docker Compose
```bash
docker-compose up --build
```

### 4. Ejecutar migraciones
```bash
docker-compose exec backend python manage.py migrate
```

### 5. Crear superusuario (opcional)
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Acceder a la aplicación

- Frontend: http://localhost:3006
- Backend API: http://localhost:8006/api/
- Admin Django: http://localhost:8006/admin/

## Estructura de Ramas Git

```
main (producción)
  ↑
test (testing)
  ↑
dev (desarrollo)
  ↑
feature/* (features individuales)
```

### Flujo de trabajo

1. Crear rama feature desde `dev`: `git checkout -b feature/nueva-funcionalidad dev`
2. Desarrollar y hacer commit
3. Crear PR hacia `dev`
4. Después de merge en `dev`, crear PR hacia `test`
5. Después de validación en `test`, crear PR hacia `main`

Ver `DEVELOPMENT.md` para detalles completos del flujo de desarrollo.

## Tests

### Ejecutar tests
```bash
# Backend
docker-compose exec backend python manage.py test

# Con coverage
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report
```

## Configuración de Umbral

El umbral de validación facial se configura mediante la variable de entorno `FACE_VERIFICATION_THRESHOLD` (default: 0.80).

Un score >= threshold resulta en `decision: true`, caso contrario `decision: false`.

## Provider de Face API

Actualmente se usa `DummyProvider` que simula la validación facial. Para reemplazarlo:

1. Implementar la interfaz `FaceVerificationProvider`
2. Actualizar `settings.py` para usar el nuevo provider
3. El método `verify()` debe retornar: `{score: float, match: bool, provider: str}`

## Notas Técnicas

- Las fotos de check-in NO se guardan en disco/DB (solo se procesan en memoria)
- Solo se guarda la foto de referencia (`photo_ref`) del empleado
- El sistema está preparado para usar S3/MinIO cambiando la configuración de `MEDIA_ROOT`
- No hay autenticación; los endpoints son abiertos (solo validación de inputs)

## Desarrollo Local (sin Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Licencia

Este proyecto es una prueba técnica.
