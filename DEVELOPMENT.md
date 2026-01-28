# Guía de Desarrollo

## Estructura de Ramas Git

El proyecto utiliza un flujo de trabajo basado en Git Flow con las siguientes ramas:

```
main (producción)
  ↑
test (testing/staging)
  ↑
dev (desarrollo)
  ↑
feature/* (features individuales)
```

### Ramas Principales

- **main**: Código en producción. Solo se actualiza mediante PRs desde `test`.
- **test**: Código en ambiente de testing/staging. Se actualiza desde `dev`.
- **dev**: Rama de desarrollo principal. Se actualiza desde `feature/*`.

### Flujo de Trabajo

1. **Crear Feature Branch**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/nombre-de-la-feature
   ```

2. **Desarrollar y Commit**
   ```bash
   git add .
   git commit -m "feat: descripción de la feature"
   ```

3. **Push y Crear PR**
   ```bash
   git push origin feature/nombre-de-la-feature
   # Crear PR hacia dev en GitHub
   ```

4. **Merge a dev**
   - Revisar PR
   - Aprobar y mergear
   - Eliminar branch `feature/*`

5. **Promover a test**
   ```bash
   git checkout test
   git merge dev
   git push origin test
   ```

6. **Promover a main**
   - Después de validación en `test`
   ```bash
   git checkout main
   git merge test
   git push origin main
   ```

## Convenciones de Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `test:` Agregar o modificar tests
- `refactor:` Refactorización de código
- `chore:` Tareas de mantenimiento

Ejemplo:
```
feat: agregar endpoint de check-in con validación facial
fix: corregir validación de código de empleado
docs: actualizar README con instrucciones de instalación
```

## Desarrollo Local

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp ../.env.example .env
# Editar .env con valores apropiados

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
# Crear .env.local con:
# REACT_APP_API_URL=http://localhost:8006/api

# Ejecutar servidor de desarrollo
npm start
```

## Testing

### Backend

```bash
cd backend

# Ejecutar todos los tests
python manage.py test

# Ejecutar tests específicos
python manage.py test attendance.tests.test_services
python manage.py test attendance.tests.test_integration

# Con coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML en htmlcov/
```

### Frontend

```bash
cd frontend

# Ejecutar tests
npm test

# Build para producción
npm run build
```

## Docker Development

### Construir y ejecutar

```bash
# Desde la raíz del proyecto
docker-compose up --build

# En modo detached
docker-compose up -d --build

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Ejecutar comandos en contenedores
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py test
```

### Limpiar contenedores

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes
docker-compose down -v
```

## Linting y Formato

### Backend (Python)

```bash
# Instalar flake8
pip install flake8

# Ejecutar linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Frontend (JavaScript/React)

El proyecto usa ESLint configurado por `react-scripts`. Los errores se muestran en la consola durante el desarrollo.

## Debugging

### Backend

- Usar `print()` o `logger.debug()` para debugging
- Configurar breakpoints en IDE (VS Code, PyCharm)
- Usar Django Debug Toolbar (agregar a INSTALLED_APPS si es necesario)

### Frontend

- Usar React DevTools
- Console.log para debugging
- Browser DevTools para inspección

## Estructura de Archivos

```
Prueba_Tecnica_CS/
├── backend/
│   ├── attendance/
│   │   ├── api/          # (futuro: endpoints específicos)
│   │   ├── services/      # Lógica de negocio
│   │   ├── repositories/  # Acceso a datos
│   │   ├── providers/     # Integraciones externas
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── ...
│   └── package.json
├── docker-compose.yml
├── README.md
└── ARCHITECTURE.md
```

## Checklist para PRs

Antes de crear un PR, verificar:

- [ ] Código sigue las convenciones del proyecto
- [ ] Tests pasan (`python manage.py test` / `npm test`)
- [ ] No hay errores de linting
- [ ] Documentación actualizada si es necesario
- [ ] Commits siguen convenciones
- [ ] Branch está actualizado con `dev`
- [ ] Descripción clara del PR

## Troubleshooting

### Error: "No module named django"
- Activar entorno virtual
- Instalar dependencias: `pip install -r requirements.txt`

### Error: "Database connection failed"
- Verificar que PostgreSQL esté corriendo
- Verificar variables de entorno en `.env`
- Verificar que la base de datos exista

### Error: "Port already in use"
- Cambiar puerto en `docker-compose.yml` o detener proceso que usa el puerto

### Error: "CORS error" en frontend
- Verificar que `CORS_ALLOWED_ORIGINS` en `settings.py` incluya la URL del frontend
- Verificar que `REACT_APP_API_URL` esté configurado correctamente
