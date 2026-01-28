# Configuración del Repositorio en GitHub

Este documento explica cómo conectar este repositorio local con GitHub y configurar las ramas principales.

## Paso 1: Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en el botón "+" en la esquina superior derecha
3. Selecciona "New repository"
4. Configura el repositorio:
   - **Name**: `Prueba_Tecnica_CS` (o el nombre que prefieras)
   - **Description**: "Sistema de Registro de Entrada con Validación Facial"
   - **Visibility**: Private o Public (según prefieras)
   - **NO marques** "Add a README file" (ya tenemos uno)
   - **NO agregues** .gitignore ni licencia (ya están incluidos)
5. Haz clic en "Create repository"

## Paso 2: Conectar Repositorio Local con GitHub

Ejecuta los siguientes comandos (reemplaza `TU_USUARIO` y `TU_REPO` con tus datos):

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# O si prefieres SSH:
# git remote add origin git@github.com:TU_USUARIO/TU_REPO.git

# Verificar que se agregó correctamente
git remote -v
```

## Paso 3: Push de las Ramas

```bash
# Push de la rama main
git push -u origin main

# Push de la rama dev
git checkout dev
git push -u origin dev

# Push de la rama test
git checkout test
git push -u origin test

# Volver a main
git checkout main
```

## Paso 4: Configurar Protección de Ramas (Opcional pero Recomendado)

En GitHub, ve a **Settings → Branches** y configura:

### Para la rama `main`:
- ✅ Require a pull request before merging
- ✅ Require approvals: 1 (o más según tu equipo)
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Include administrators

### Para la rama `test`:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

### Para la rama `dev`:
- Opcional: Puedes dejar sin protección o con protección mínima

## Paso 5: Verificar Configuración

```bash
# Ver todas las ramas locales y remotas
git branch -a

# Ver el estado del repositorio
git status

# Ver los remotes configurados
git remote -v
```

## Estructura de Ramas Actual

```
* main  (rama principal de producción)
  dev   (rama de desarrollo)
  test  (rama de testing/staging)
```

## Próximos Pasos

1. Crear feature branches desde `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/nombre-de-la-feature
   ```

2. Trabajar en la feature y hacer commits

3. Crear Pull Request hacia `dev` en GitHub

4. Después de merge, promover a `test` y luego a `main`

Para más detalles sobre el flujo de trabajo, consulta `.github/BRANCHES.md`
