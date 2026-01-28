# Instrucciones para hacer Push a GitHub

## Opción 1: Usar Token de Acceso Personal (Recomendado)

### Paso 1: Crear Token en GitHub

1. Ve a: https://github.com/settings/tokens
2. Haz clic en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre: "Prueba_Tecnica_CS"
4. Selecciona el scope: **repo** (acceso completo a repositorios)
5. Haz clic en "Generate token"
6. **COPIA EL TOKEN** (solo se muestra una vez)

### Paso 2: Hacer Push usando el Token

Cuando Git te pida credenciales:
- **Username**: `inglog11`
- **Password**: Pega el token que copiaste (NO tu contraseña de GitHub)

O ejecuta estos comandos:

```bash
# Push de main
git push -u origin main

# Cuando pida usuario: inglog11
# Cuando pida contraseña: pega el token
```

## Opción 2: Usar SSH (Alternativa)

### Paso 1: Generar clave SSH (si no tienes una)

```bash
ssh-keygen -t ed25519 -C "tu_email@example.com"
```

### Paso 2: Agregar clave SSH a GitHub

1. Copia tu clave pública:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Ve a: https://github.com/settings/keys
3. Haz clic en "New SSH key"
4. Pega la clave y guarda

### Paso 3: Cambiar remote a SSH

```bash
git remote set-url origin git@github.com:inglog11/facial_validation_logp.git
```

### Paso 4: Hacer Push

```bash
git push -u origin main
```

## Opción 3: Usar GitHub CLI (gh)

Si tienes GitHub CLI instalado:

```bash
gh auth login
git push -u origin main
```

## Después del Push Inicial

Una vez que hayas hecho push de `main`, haz push de las otras ramas:

```bash
# Push de dev
git checkout dev
git push -u origin dev

# Push de test
git checkout test
git push -u origin test

# Volver a main
git checkout main
```

## Verificar

```bash
# Ver todas las ramas remotas
git branch -r

# Ver estado
git status
```
