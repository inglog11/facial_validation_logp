# Cómo Crear un Token de Acceso Personal en GitHub

Los tokens de acceso personal están en la configuración de tu **cuenta de usuario**, no en la configuración del repositorio.

## Pasos Detallados:

### Opción 1: Desde la página actual (Settings del repositorio)

1. En la parte superior derecha de GitHub, haz clic en tu **foto de perfil** (ícono de usuario)
2. En el menú desplegable, haz clic en **"Settings"** (Configuración)
3. En el menú lateral izquierdo, desplázate hacia abajo hasta encontrar **"Developer settings"**
4. Haz clic en **"Developer settings"**
5. En el submenú, haz clic en **"Personal access tokens"**
6. Haz clic en **"Tokens (classic)"** o **"Fine-grained tokens"** (recomiendo classic para simplicidad)
7. Haz clic en **"Generate new token"** → **"Generate new token (classic)"**

### Opción 2: Acceso Directo

Ve directamente a esta URL:
**https://github.com/settings/tokens**

O si prefieres tokens fine-grained:
**https://github.com/settings/tokens/new**

### Configuración del Token:

1. **Note** (Nota): Dale un nombre descriptivo, ej: "Prueba_Tecnica_CS"
2. **Expiration** (Expiración): Elige cuánto tiempo quieres que dure (puedes poner "No expiration" si quieres que no expire)
3. **Select scopes** (Seleccionar permisos):
   - ✅ Marca **"repo"** (esto da acceso completo a repositorios)
   - Esto incluye automáticamente: repo:status, repo_deployment, public_repo, repo:invite, security_events
4. Haz clic en **"Generate token"** (Generar token)
5. **¡IMPORTANTE!** Copia el token inmediatamente (solo se muestra una vez)
   - Se verá algo como: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Usar el Token:

Cuando hagas `git push`, Git te pedirá credenciales:
- **Username**: `inglog11`
- **Password**: Pega el token que copiaste (NO tu contraseña de GitHub)

## Alternativa: Usar GitHub CLI (más fácil)

Si tienes GitHub CLI instalado, puedes autenticarte más fácilmente:

```bash
# Instalar GitHub CLI (si no lo tienes)
brew install gh

# Autenticarse
gh auth login

# Selecciona GitHub.com → HTTPS → Login with a web browser
```

Después de autenticarte con `gh auth login`, podrás hacer push sin problemas.
