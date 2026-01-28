# Estructura de Ramas Git

Este proyecto utiliza un flujo de trabajo basado en Git Flow con las siguientes ramas:

## Ramas Principales

- **main**: Rama de producción. Contiene código estable y listo para producción.
- **dev**: Rama de desarrollo. Contiene código en desarrollo activo.
- **test**: Rama de testing/staging. Contiene código listo para pruebas antes de producción.

## Flujo de Trabajo

```
main (producción)
  ↑
test (testing/staging)
  ↑
dev (desarrollo)
  ↑
feature/* (features individuales)
```

### Crear Feature Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/nombre-de-la-feature
```

### Desarrollar y Commit

```bash
git add .
git commit -m "feat: descripción de la feature"
```

### Crear Pull Request

1. Push de la feature branch:
   ```bash
   git push origin feature/nombre-de-la-feature
   ```

2. Crear Pull Request en GitHub hacia `dev`

3. Después de revisión y aprobación, mergear a `dev`

### Promover a test

```bash
git checkout test
git merge dev
git push origin test
```

### Promover a main

Después de validación en `test`:

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

## Configuración Inicial de GitHub

Para conectar este repositorio local con GitHub:

1. Crear un nuevo repositorio en GitHub (sin inicializar con README)

2. Conectar el repositorio local:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   ```

3. Push de todas las ramas:
   ```bash
   git push -u origin main
   git push -u origin dev
   git push -u origin test
   ```

4. Configurar protección de ramas en GitHub:
   - Settings → Branches
   - Agregar reglas para `main` y `test`:
     - Require pull request reviews before merging
     - Require status checks to pass before merging
     - Require branches to be up to date before merging
