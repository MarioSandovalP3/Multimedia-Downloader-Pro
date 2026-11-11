# Multimedia Downloader Pro

Una aplicación de escritorio moderna, ligera y fácil de usar desarrollada en **Python** con **Tkinter** y potenciada por **yt-dlp**. Permite descargar vídeos, reels, publicaciones y listas de reproducción de YouTube, TikTok, Instagram, Facebook y más de 1800 sitios web compatibles.

---

## Características Principales

| Característica | Descripción |
|----------------|-------------|
| **Amplia compatibilidad** | Soporta YouTube, TikTok, Instagram, Facebook y miles de plataformas gracias a yt-dlp (más de 1800 sitios web). |
| 🎞️ **Múltiples calidades** | Opción para descargar la mejor calidad disponible, limitar a resoluciones específicas (1080p, 720p) o extraer únicamente el audio en formato MP3. |
| **Listas de reproducción** | Casilla de verificación para descargar listas de reproducción completas de forma opcional. |
| **Autenticación por cookies** | Permite utilizar las cookies de tu navegador web favorito (Chrome, Firefox, Edge, Safari, Brave, Opera) para descargar contenido privado, restringido o que requiera iniciar sesión. |
| **Interfaz gráfica intuitiva** | Botón rápido para pegar desde el portapapeles, selector de carpeta de destino con explorador visual, barra de progreso en tiempo real con velocidad y ETA, y panel de registro (Log) detallado. |
| **Multihilos (Threading)** | Evita que la interfaz se congele durante las descargas pesadas. |

---

## Requisitos previos

Antes de instalar, asegúrate de tener lo siguiente:

| Requisito | Versión | Notas |
|-----------|---------|-------|
| **Python** | 3.10 o superior | [Descargar](https://www.python.org/downloads/) |
| **yt-dlp** | Última versión | Motor de descarga (se instala con pip) |
| **FFmpeg** | Cualquier reciente | Obligatorio para combinar vídeo/audio y convertir a MP3 |
| **Deno** | Cualquier reciente | Recomendado para desafíos de JavaScript de YouTube |

### Instalar herramientas del sistema (no son paquetes de Python)

**Windows (PowerShell):**
```powershell
winget install Gyan.FFmpeg
winget install DenoLand.Deno
```

**macOS:**
```bash
brew install ffmpeg
brew install deno
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install ffmpeg
# Deno:
curl -fsSL https://deno.land/x/install/install.sh | sh -s v1.xx.x
```

Verifica que estén en el PATH:
```powershell
ffmpeg -version
deno --version
```

---

## Instalación

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

### 1. Clonar el repositorio

```bash
git clone https://github.com/MarioSandovalP3/Multimedia-Downloader-Pro.git
cd Multimedia-Downloader-Pro
```

### 2. Crear y activar el entorno virtual

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cuando se active, verás `(.venv)` al inicio de la consola. Para salir: `deactivate`.

### 3. Instalar dependencias de Python

```powershell
py -m pip install -U -r requirements.txt
```

El archivo `requirements.txt` contiene:
```
yt-dlp[default]>=2025.1.0
```

> El extra `[default]` instala los componentes **EJS** necesarios para los desafíos de JavaScript de YouTube.

### 4. Ejecutar la aplicación

```powershell
py app.py
```

En Windows también puedes hacer doble clic en `iniciar_windows.bat`.

---

## Estructura del proyecto

```
multimedia_downloader_pro/
├── app.py                 # Código principal de la aplicación
├── requirements.txt       # Dependencias de Python (pip)
├── iniciar_windows.bat    # Script de inicio rápido para Windows
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

---

## Uso

1. Ejecuta `py app.py` (o `iniciar_windows.bat`).
2. Pega la URL del vídeo, reel, publicación o lista de reproducción.
3. Selecciona la calidad deseada (Mejor calidad disponible, hasta 1080p, hasta 720p o Solo audio MP3).
4. Marca "Descargar lista de reproducción completa" si aplica.
5. Elige la carpeta de destino con el explorador visual.
6. Haz clic en **Descargar**.
7. Observa el progreso en tiempo real con velocidad y ETA en el panel de registro.

---

## Cuando notes que un día una plataforma deja de descargar, no significa que el script se haya roto para siempre, sino que necesitas actualizar el motor ejecutando: ##
```bash
pip install --upgrade yt-dlp
```

## Para convertir tu script de Python en un archivo ejecutable .exe para Windows que se pueda abrir con un doble clic (sin necesidad de instalar Python ni dependencias manualmente en otra PC), la herramienta estándar y más recomendada es PyInstaller. ##

### 1. Instalar PyInstaller ###
Abre tu terminal (CMD o PowerShell) y asegúrate de tener instalado PyInstaller ejecutando:

```bash
pip install --upgrade pyinstaller
```

### 2. Generar el ejecutable ###
Navega en tu terminal hasta la carpeta donde tienes guardado tu script (por ejemplo, app.py) y ejecuta el siguiente comando:
```bash
python pyinstaller --noconsole --onefile app.py
```
--onefile: Empaqueta todo en un único archivo .exe independiente y fácil de distribuir.

--noconsole: Oculta la ventana negra de la terminal (CMD) al abrir la aplicación, haciendo que solo se vea la interfaz gráfica moderna que diseñamos. (Si en algún momento necesitas ver los errores de consola para depurar, puedes quitar este parámetro).

### 3. ¿Dónde se guarda el archivo? ###
Una vez que el proceso termine (puede tardar unos segundos), verás varias carpetas nuevas en tu directorio de trabajo:

Entra a la carpeta dist.

¡Listo! Dentro encontrarás tu archivo app.exe.

## Consejos útiles antes de distribuirlo: ##
Icono personalizado (Opcional): Si quieres que tu .exe tenga un icono profesional en lugar del predeterminado de Python, puedes agregarlo con la opción --icon:
```bash
python -m PyInstaller --noconsole --onefile --icon="icon.ico" --name="Multimedia Downloader Pro" app.py

```
Dependencias externas: Recuerda que si tu aplicación requiere FFmpeg, este no se incluye automáticamente dentro del .exe por cuestiones de tamaño. Deberás asegurarte de que los usuarios finales tengan FFmpeg en su ordenador o incluirlo junto con tu ejecutable si planean descargar MP3 o vídeos pesados.


## Solución de problemas

| Problema | Solución |
|----------|----------|
| `Requested format is not available` | Actualiza yt-dlp: `py -m pip install -U "yt-dlp[default]"` |
| Error de FFmpeg | Ejecuta `ffmpeg -version` en una terminal nueva para confirmar que está en PATH |
| Error de JavaScript runtime | Ejecuta `deno --version` y actualiza yt-dlp y sus componentes EJS |
| Contenido privado o restringido | Usa la autenticación por cookies de tu navegador (Chrome, Firefox, Edge, etc.) |
| La UI se congela durante la descarga | No debería pasar; la app usa threading para mantener la interfaz fluida |

---

## Aviso legal

Esta herramienta está diseñada para descargar contenido del que tengas derecho legal o permiso del autor. **No la uses para eludir restricciones de copyright, geobloqueos o términos de servicio de las plataformas.** El usuario es responsable del uso que le dé a esta aplicación.

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto:

1. Haz un **fork** del repositorio.
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`.
3. Realiza tus cambios y haz commit: `git commit -m "feat: descripción"`.
4. Sube tus cambios: `git push origin feature/nueva-funcionalidad`.
5. Abre un **Pull Request**.

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

## ☕ Apóyame

Si este proyecto te fue útil, puedes apoyarme con una donación:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/coderdev)

---




