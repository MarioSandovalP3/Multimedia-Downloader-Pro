import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
import urllib.request
import io
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
from PIL import Image

APP_NAME = "Multimedia Downloader Pro"
APP_VERSION = "1.0.0"
CONFIG_DIR = Path.home() / ".multimedia_downloader_pro"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / "Multimedia Downloader"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

TRANSLATIONS = {
    'es': {
        'app_title': "Multimedia Downloader Pro",
        'sidebar_title': "⬇ MEDIA PRO",
        'sidebar_subtitle': "VIDEO & AUDIO DOWNLOADER",
        'nav_download': "⇩ Descargar",
        'nav_activity': "◷ Actividad",
        'nav_settings': "⚙ Configuración",
        'sys_status': "ESTADO DEL SISTEMA",
        'checking_deps': "Comprobando dependencias…",
        'donate_btn': "🤝 Donar / Contribuir",
        'disclaimer': "Herramienta para descarga de contenido propio o de dominio público. El desarrollador no se responsabiliza por el uso indebido de material con derechos de autor.",
        'dl_title': "Descargar contenido",
        'dl_subtitle': "Pega un enlace y configura las opciones de descarga.",
        'url_label': "URL DEL CONTENIDO",
        'url_placeholder': "https://www.youtube.com/watch?v=…",
        'paste_btn': "Pegar",
        'opts_label': "OPCIONES DE DESCARGA",
        'quality_label': "Calidad y formato",
        'playlist_label': "Lista de reproducción",
        'playlist_check': "Descargar lista completa",
        'cookies_label': "Cookies del navegador",
        'status_ready': "Listo para descargar",
        'dl_btn': "⬇ INICIAR DESCARGA",
        'dl_btn_downloading': "DESCARGANDO…",
        'open_folder_btn': "Abrir carpeta",
        'note_text': "Nota: la disponibilidad depende del sitio. Algunos formatos requieren FFmpeg.",
        'act_title': "Actividad de descargas",
        'act_subtitle': "Consulta las descargas recientes y sus detalles.",
        'records_saved': "registros guardados",
        'update_btn': "Actualizar",
        'clear_hist_btn': "Borrar historial",
        'no_records': "Todavía no hay descargas registradas.\nAparecerán aquí automáticamente.",
        'status_completed': "Completada",
        'status_progress': "En curso",
        'status_error': "Error",
        'status_unknown': "Desconocido",
        'settings_title': "Configuración",
        'settings_subtitle': "Personaliza el comportamiento de la aplicación.",
        'appearance_label': "APARIENCIA",
        'theme_label': "Tema de la aplicación",
        'downloads_label': "DESCARGAS",
        'default_folder': "Carpeta predeterminada",
        'change_btn': "Cambiar",
        'default_quality': "Calidad predeterminada",
        'playlist_default': "Incluir listas de reproducción por defecto",
        'privacy_label': "PRIVACIDAD Y ACCESO",
        'cookies_text': "Navegador del que se leerán cookies",
        'save_btn': "Guardar configuración",
        'reset_btn': "Restaurar valores",
        'config_path': "Configuración:",
        'lang_label': "Idioma de la aplicación",
        'preview_label': "VISTA PREVIA DETECTADA",
        'channel_label': "Canal:",
        'duration_label': "Duración:",
        'loading_preview': "⏳ Obteniendo información...",
        'no_image': "Sin imagen",
        'img_loading': "Cargando imagen...",
        'img_error': "Imagen no disponible",
        'msg_invalid_url': "Enlace inválido",
        'msg_invalid_url_text': "Introduce una URL válida (http:// o https://).",
        'msg_downloading': "Descarga en curso",
        'msg_downloading_text': "Espera a que termine la descarga actual.",
        'msg_completed': "Descarga completada",
        'msg_error': "Error de descarga",
        'msg_clear_hist': "Borrar historial",
        'msg_clear_hist_text': "¿Eliminar todos los registros de actividad?",
        'msg_reset': "Restaurar",
        'msg_reset_text': "¿Restaurar las preferencias iniciales?",
        'msg_clipboard': "Portapapeles",
        'msg_clipboard_text': "No hay texto en el portapapeles.",
        'status_downloading': "Descargando",
        'status_processing': "Procesando archivo…",
        'status_preparing': "Preparando descarga…",
        'status_fetching': "Obteniendo información...",
        'status_failed_preview': "No se pudo obtener la vista previa.",
        'history_initiated': "Descarga iniciada",
        'history_completed': "Descarga completada",
        'history_error': "La descarga terminó con un error",
        'ffmpeg_avail': "Disponible",
        'ffmpeg_not': "No instalado",
        'deno_avail': "Disponible",
        'deno_opt': "Opcional",
        'quality_best': "Mejor disponible",
        'quality_4k': "Vídeo hasta 2160p (4K)",
        'quality_1080': "Vídeo hasta 1080p",
        'quality_720': "Vídeo hasta 720p",
        'quality_mp3': "Solo audio (MP3)",
        'quality_m4a': "Solo audio (M4A)",
        'unknown_title': "Título desconocido",
        'unknown_channel': "Desconocido",
        'unknown_duration': "Duración desconocida",
        'playlist_title': "Lista de reproducción",
        'playlist_elements': "elementos",
        'min': "min",
        'sec': "seg",
        'various': "varios",
        'theme_dark': "Oscuro",
        'theme_light': "Claro",
        'theme_system': "Sistema",
        'lang_es': "Español",
        'lang_en': "Inglés",
        'cookies_none': "Ninguno"
    },
    'en': {
        'app_title': "Multimedia Downloader Pro",
        'sidebar_title': "⬇ MEDIA PRO",
        'sidebar_subtitle': "VIDEO & AUDIO DOWNLOADER",
        'nav_download': "⇩ Download",
        'nav_activity': "◷ Activity",
        'nav_settings': "⚙ Settings",
        'sys_status': "SYSTEM STATUS",
        'checking_deps': "Checking dependencies…",
        'donate_btn': "🤝 Donate / Contribute",
        'disclaimer': "Tool for downloading own or public domain content. Developer is not responsible for unauthorized downloading of copyrighted material.",
        'dl_title': "Download content",
        'dl_subtitle': "Paste a link and configure download options.",
        'url_label': "CONTENT URL",
        'url_placeholder': "https://www.youtube.com/watch?v=…",
        'paste_btn': "Paste",
        'opts_label': "DOWNLOAD OPTIONS",
        'quality_label': "Quality and format",
        'playlist_label': "Playlist",
        'playlist_check': "Download full playlist",
        'cookies_label': "Browser cookies",
        'status_ready': "Ready to download",
        'dl_btn': "⬇ START DOWNLOAD",
        'dl_btn_downloading': "DOWNLOADING…",
        'open_folder_btn': "Open folder",
        'note_text': "Note: availability depends on the site. Some formats require FFmpeg.",
        'act_title': "Download activity",
        'act_subtitle': "Check recent downloads and their details.",
        'records_saved': "saved records",
        'update_btn': "Update",
        'clear_hist_btn': "Clear history",
        'no_records': "No downloads registered yet.\nThey will appear here automatically.",
        'status_completed': "Completed",
        'status_progress': "In progress",
        'status_error': "Error",
        'status_unknown': "Unknown",
        'settings_title': "Settings",
        'settings_subtitle': "Customize the application behavior.",
        'appearance_label': "APPEARANCE",
        'theme_label': "App theme",
        'downloads_label': "DOWNLOADS",
        'default_folder': "Default folder",
        'change_btn': "Change",
        'default_quality': "Default quality",
        'playlist_default': "Include playlists by default",
        'privacy_label': "PRIVACY & ACCESS",
        'cookies_text': "Browser to read cookies from",
        'save_btn': "Save settings",
        'reset_btn': "Restore defaults",
        'config_path': "Config:",
        'lang_label': "Application language",
        'preview_label': "PREVIEW DETECTED",
        'channel_label': "Channel:",
        'duration_label': "Duration:",
        'loading_preview': "⏳ Getting link info...",
        'no_image': "No image",
        'img_loading': "Loading image...",
        'img_error': "Image not available",
        'msg_invalid_url': "Invalid link",
        'msg_invalid_url_text': "Enter a valid URL (http:// or https://).",
        'msg_downloading': "Download in progress",
        'msg_downloading_text': "Wait for the current download to finish.",
        'msg_completed': "Download completed",
        'msg_error': "Download error",
        'msg_clear_hist': "Clear history",
        'msg_clear_hist_text': "Delete all activity records?",
        'msg_reset': "Restore",
        'msg_reset_text': "Restore initial preferences?",
        'msg_clipboard': "Clipboard",
        'msg_clipboard_text': "No text in clipboard.",
        'status_downloading': "Downloading",
        'status_processing': "Processing file…",
        'status_preparing': "Preparing download…",
        'status_fetching': "Getting link info...",
        'status_failed_preview': "Could not get preview.",
        'history_initiated': "Download initiated",
        'history_completed': "Download completed",
        'history_error': "Download ended with an error",
        'ffmpeg_avail': "Available",
        'ffmpeg_not': "Not installed",
        'deno_avail': "Available",
        'deno_opt': "Optional",
        'quality_best': "Best available",
        'quality_4k': "Video up to 2160p (4K)",
        'quality_1080': "Video up to 1080p",
        'quality_720': "Video up to 720p",
        'quality_mp3': "Audio only (MP3)",
        'quality_m4a': "Audio only (M4A)",
        'unknown_title': "Unknown title",
        'unknown_channel': "Unknown",
        'unknown_duration': "Unknown duration",
        'playlist_title': "Playlist",
        'playlist_elements': "elements",
        'min': "min",
        'sec': "sec",
        'various': "various",
        'theme_dark': "Dark",
        'theme_light': "Light",
        'theme_system': "System",
        'lang_es': "Spanish",
        'lang_en': "English",
        'cookies_none': "None"
    }
}

def safe_read_json(path, default):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, TypeError):
        return default

def safe_write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp.replace(path)

def valid_url(value):
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

class MultimediaDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} | v{APP_VERSION}")
        
        # 1. DETECCIÓN DE PANTALLA Y CONFIGURACIÓN RESPONSIVA
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.is_small_screen = (screen_width <= 1366 or screen_height <= 768)
        
        # 2. CONFIGURAR TAMAÑOS BASE SEGÚN PANTALLA
        if self.is_small_screen:
            self.geometry("900x600")
            self.minsize(800, 500)
            self.FONT_TITLE = ("Segoe UI", 18, "bold")
            self.FONT_SUBTITLE = ("Segoe UI", 11)
            self.FONT_LABEL = ("Segoe UI", 11, "bold")
            self.FONT_TEXT = ("Segoe UI", 11)
            self.FONT_SMALL = ("Segoe UI", 10)
            self.FONT_TINY = ("Segoe UI", 9)
            self.SIDEBAR_WIDTH = 180
            self.ENTRY_HEIGHT = 36
            self.BUTTON_HEIGHT = 38
            self.PADDING = 12
            self.THUMB_SIZE = (120, 68)
        else:
            self.geometry("1120x780")
            self.minsize(940, 680)
            self.FONT_TITLE = ("Segoe UI", 24, "bold")
            self.FONT_SUBTITLE = ("Segoe UI", 12)
            self.FONT_LABEL = ("Segoe UI", 12, "bold")
            self.FONT_TEXT = ("Segoe UI", 12)
            self.FONT_SMALL = ("Segoe UI", 11)
            self.FONT_TINY = ("Segoe UI", 10)
            self.SIDEBAR_WIDTH = 225
            self.ENTRY_HEIGHT = 42
            self.BUTTON_HEIGHT = 46
            self.PADDING = 18
            self.THUMB_SIZE = (160, 90)

        # 3. FORZAR APERTURA EN PANTALLA COMPLETA (MAXIMIZADA) DE MANERA ROBUSTA
        self.after(50, self._force_maximize)

        self.config_data = safe_read_json(CONFIG_FILE, {})
        self.history = safe_read_json(HISTORY_FILE, [])
        if not isinstance(self.history, list):
            self.history = []

        self.lang = self.config_data.get("language", "es")
        self.events = queue.Queue()
        self.active_download = False
        self.download_thread = None
        self.current_page = None

        self.url_var = ctk.StringVar()
        self.folder_var = ctk.StringVar(value=self.config_data.get("folder", str(DEFAULT_DOWNLOAD_DIR)))
        self.quality_var = ctk.StringVar(value=self.config_data.get("quality", self.t('quality_best')))
        self.cookies_var = ctk.StringVar(value=self.config_data.get("cookies_browser", self.t('cookies_none')))
        self.playlist_var = ctk.BooleanVar(value=self.config_data.get("playlist", False))
        self.theme_var = ctk.StringVar(value=self.config_data.get("theme", self.t('theme_dark')))
        self.status_var = ctk.StringVar(value=self.t('status_ready'))
        self.progress_var = ctk.DoubleVar(value=0)

        self.preview_after_id = None
        self.preview_debounce_ms = 600
        
        self.last_preview_info = None
        self.last_preview_url = None
        self.last_thumbnail_image = None
        self.preview_container = None
        self.preview_request_id = 0
        self.preview_trace_id = self.url_var.trace_add("write", self._on_url_change)
        self.thumb_label = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_navigation()
        self._build_content()
        self.show_page("download")
        self.after(120, self._process_events)
        self.after(700, self._check_dependencies)

    def _force_maximize(self):
        try:
            self.state('zoomed')  # Windows y algunos Linux
        except Exception:
            try:
                self.attributes('-zoomed', True)  # Otros entornos Linux
            except Exception:
                self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS['es']).get(key, key)

    def get_cookies_values(self):
        return [self.t('cookies_none'), "chrome", "edge", "firefox", "brave", "opera", "vivaldi"]

    def get_quality_values(self):
        return [self.t('quality_best'), self.t('quality_4k'), self.t('quality_1080'), self.t('quality_720'), self.t('quality_mp3'), self.t('quality_m4a')]

    # ---------------------- DATA ----------------------
    def save_settings(self):
        self.config_data = {
            "folder": self.folder_var.get().strip() or str(DEFAULT_DOWNLOAD_DIR),
            "quality": self.quality_var.get(),
            "cookies_browser": self.cookies_var.get(),
            "playlist": bool(self.playlist_var.get()),
            "theme": self.theme_var.get(),
            "language": self.lang,
        }
        safe_write_json(CONFIG_FILE, self.config_data)

    def add_history(self, url, status, details=""):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing_index = -1
        for i, item in enumerate(self.history):
            if item.get("url") == url:
                existing_index = i
                break
        
        if existing_index != -1:
            self.history[existing_index]["status"] = status
            self.history[existing_index]["details"] = details
            self.history[existing_index]["date"] = current_date
            entry = self.history.pop(existing_index)
            self.history.insert(0, entry)
        else:
            self.history.insert(0, {"date": current_date, "url": url, "status": status, "details": details})
            
        self.history = self.history[:500]
        safe_write_json(HISTORY_FILE, self.history)
        self.events.put(("history_changed", None))

    # ---------------------- MAIN LAYOUT ----------------------
    def _build_navigation(self):
        self.sidebar = ctk.CTkFrame(self, width=self.SIDEBAR_WIDTH, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title_font = ("Segoe UI", 16, "bold") if self.is_small_screen else ("Segoe UI", 20, "bold")
        self.lbl_sidebar_title = ctk.CTkLabel(self.sidebar, text=self.t('sidebar_title'), font=title_font)
        self.lbl_sidebar_title.pack(anchor="w", padx=15, pady=(20, 3))
        
        self.lbl_sidebar_subtitle = ctk.CTkLabel(self.sidebar, text=f"{self.t('sidebar_subtitle')} · v{APP_VERSION}", font=self.FONT_TINY, text_color="gray")
        self.lbl_sidebar_subtitle.pack(anchor="w", padx=15, pady=(0, 15))

        self.nav_buttons = {}
        nav_items = [("download", self.t('nav_download')), ("activity", self.t('nav_activity')), ("settings", self.t('nav_settings'))]
        for page, label in nav_items:
            btn_h = 36 if self.is_small_screen else 40
            button = ctk.CTkButton(self.sidebar, text=label, height=btn_h, anchor="w", corner_radius=8, fg_color="transparent", text_color=("gray15", "gray90"), hover_color=("gray85", "gray25"), command=lambda p=page: self.show_page(p))
            button.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[page] = button

        ctk.CTkFrame(self.sidebar, height=1, fg_color=("gray80", "gray30")).pack(fill="x", padx=15, pady=(10, 8))
        
        self.lbl_sys_status = ctk.CTkLabel(self.sidebar, text=self.t('sys_status'), font=self.FONT_TINY, text_color="gray")
        self.lbl_sys_status.pack(anchor="w", padx=15, pady=(0, 5))
        
        wrap_len = 150 if self.is_small_screen else 180
        self.dependencies_label = ctk.CTkLabel(self.sidebar, text=self.t('checking_deps'), font=self.FONT_TINY, text_color="gray", justify="left", wraplength=wrap_len)
        self.dependencies_label.pack(anchor="w", padx=15)

        ctk.CTkFrame(self.sidebar, height=1, fg_color="transparent").pack(expand=True, fill="both")

        btn_donate_h = 32 if self.is_small_screen else 36
        self.donate_button = ctk.CTkButton(self.sidebar, text=self.t('donate_btn'), height=btn_donate_h, corner_radius=6, fg_color="#f4efe7", hover_color="#CFCBC4", font=self.FONT_SMALL, text_color="black", command=self.open_donation)
        self.donate_button.pack(fill="x", padx=15, pady=(0, 10))

        disclaimer_font = self.FONT_TINY if self.is_small_screen else self.FONT_SMALL
        self.lbl_disclaimer = ctk.CTkLabel(self.sidebar, text=self.t('disclaimer'), font=disclaimer_font, text_color="gray", justify="left", wraplength=wrap_len)
        self.lbl_disclaimer.pack(anchor="w", padx=15, pady=(0, 15))

    def _build_content(self):
        pad_x = 15 if self.is_small_screen else 20
        pad_y = 15 if self.is_small_screen else 20
        self.content = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=pad_x, pady=pad_y)
        self.content.grid_columnconfigure(0, weight=1)

    def show_page(self, page):
        if self.current_page == "download" and page != "download":
            self.preview_request_id += 1
            if self.preview_after_id is not None:
                try: self.after_cancel(self.preview_after_id)
                except Exception: pass
                self.preview_after_id = None

        self.current_page = page
        for key, button in self.nav_buttons.items():
            selected = key == page
            button.configure(
                text=self.t('nav_download') if key == 'download' else (self.t('nav_activity') if key == 'activity' else self.t('nav_settings')),
                fg_color=("#DCEBFF", "#17365D") if selected else "transparent",
                text_color=("#12345A", "#FFFFFF") if selected else ("gray15", "gray90")
            )
        for child in self.content.winfo_children():
            child.destroy()

        if page == "download": self._build_download_page()
        elif page == "activity": self._build_activity_page()
        elif page == "settings": self._build_settings_page()

    def _heading(self, title, subtitle):
        ctk.CTkLabel(self.content, text=title, font=self.FONT_TITLE).pack(anchor="w", fill="x")
        ctk.CTkLabel(self.content, text=subtitle, font=self.FONT_SUBTITLE, text_color="gray").pack(anchor="w", fill="x", pady=(3, 12))

    def _card(self, parent=None):
        return ctk.CTkFrame(parent or self.content, corner_radius=12, border_width=1, border_color=("gray85", "gray25"))

    # ---------------------- DOWNLOAD PAGE ----------------------
    def _build_download_page(self):
        self._heading(self.t('dl_title'), self.t('dl_subtitle'))

        link_card = self._card()
        link_card.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(link_card, text=self.t('url_label'), font=self.FONT_LABEL, text_color="gray").pack(anchor="w", padx=self.PADDING, pady=(10, 5))
        link_row = ctk.CTkFrame(link_card, fg_color="transparent")
        link_row.pack(fill="x", padx=self.PADDING, pady=(0, 10))
        self.url_entry = ctk.CTkEntry(link_row, textvariable=self.url_var, height=self.ENTRY_HEIGHT, placeholder_text=self.t('url_placeholder'))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.url_var.trace_add("write", self._on_url_change)
        ctk.CTkButton(link_row, text=self.t('paste_btn'), width=80, height=self.ENTRY_HEIGHT, command=self.paste_url).pack(side="right")

        options = self._card()
        options.pack(fill="x", pady=(0, 10))
        options.grid_columnconfigure((0, 1, 2), weight=1, uniform="download_options")

        ctk.CTkLabel(options, text=self.t('opts_label'), font=self.FONT_LABEL, text_color="gray").grid(row=0, column=0, columnspan=3, sticky="w", padx=self.PADDING, pady=(10, 5))

        quality_frame = ctk.CTkFrame(options, fg_color="transparent")
        quality_frame.grid(row=1, column=0, sticky="ew", padx=(self.PADDING, 5), pady=(0, 10))
        quality_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(quality_frame, text=self.t('quality_label'), font=self.FONT_SMALL).pack(anchor="w", pady=(0, 4))
        self.quality_combo = ctk.CTkComboBox(quality_frame, variable=self.quality_var, state="readonly", values=self.get_quality_values(), height=self.ENTRY_HEIGHT)
        self.quality_combo.pack(fill="x", expand=True)

        playlist_frame = ctk.CTkFrame(options, fg_color="transparent")
        playlist_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))
        playlist_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(playlist_frame, text=self.t('playlist_label'), font=self.FONT_SMALL).pack(anchor="w", pady=(0, 4))
        ctk.CTkCheckBox(playlist_frame, text=self.t('playlist_check'), variable=self.playlist_var).pack(anchor="w", pady=5)

        cookies_frame = ctk.CTkFrame(options, fg_color="transparent")
        cookies_frame.grid(row=1, column=2, sticky="ew", padx=(5, self.PADDING), pady=(0, 10))
        cookies_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(cookies_frame, text=self.t('cookies_label'), font=self.FONT_SMALL).pack(anchor="w", pady=(0, 4))
        self.cookies_combo = ctk.CTkComboBox(cookies_frame, variable=self.cookies_var, state="readonly", values=self.get_cookies_values(), height=self.ENTRY_HEIGHT)
        self.cookies_combo.pack(fill="x", expand=True)

        progress_card = self._card()
        progress_card.pack(fill="x", pady=(0, 10))
        status_row = ctk.CTkFrame(progress_card, fg_color="transparent")
        status_row.pack(fill="x", padx=self.PADDING, pady=(8, 4))
        ctk.CTkLabel(status_row, textvariable=self.status_var, font=self.FONT_TEXT).pack(side="left", fill="x", expand=True)
        self.progress_percent = ctk.CTkLabel(status_row, text="0%", text_color="gray", font=self.FONT_SMALL)
        self.progress_percent.pack(side="right")
        self.progress_bar = ctk.CTkProgressBar(progress_card)
        self.progress_bar.pack(fill="x", padx=self.PADDING, pady=(0, 10))
        self.progress_bar.set(0)

        self.action_row = ctk.CTkFrame(self.content, fg_color="transparent")
        self.action_row.pack(fill="x")
        self.download_button = ctk.CTkButton(self.action_row, text=self.t('dl_btn'), height=self.BUTTON_HEIGHT, font=self.FONT_LABEL, command=self.start_download)
        self.open_folder_button = ctk.CTkButton(self.action_row, text=self.t('open_folder_btn'), width=130, height=self.BUTTON_HEIGHT, fg_color=("gray75", "gray25"), text_color=("gray10", "white"), command=self.open_download_folder)
        self.open_folder_button.pack(side="right")

        wrap_len = 500 if self.is_small_screen else 700
        ctk.CTkLabel(self.content, text=self.t('note_text'), text_color="gray", font=self.FONT_TINY, wraplength=wrap_len).pack(anchor="w", fill="x", pady=(10, 12))

        self.after(100, self._restore_preview_if_available)

    def _restore_preview_if_available(self):
        current_url = self.url_var.get().strip()
        if (self.last_preview_info is not None and self.last_preview_url == current_url and valid_url(current_url)):
            if not self.download_button.winfo_ismapped():
                self.download_button.pack(side="left", fill="x", expand=True, padx=(0, 8))
            self.preview_container = ctk.CTkFrame(self.content, fg_color="transparent")
            self.preview_container.pack(fill="x", pady=(0, 10), before=self.action_row)
            self._rebuild_preview_ui(self.last_preview_info)
        elif valid_url(current_url):
            self._on_url_change()

    def _rebuild_preview_ui(self, info):
        is_playlist = info.get('_type') == 'playlist'
        if is_playlist:
            title = info.get('title', self.t('playlist_title'))
            uploader = f"{info.get('uploader', self.t('unknown_channel'))} · {info.get('playlist_count', '?')} {self.t('playlist_elements')}"
            duration_str = self.t('playlist_title')
        else:
            title = info.get('title', self.t('unknown_title'))
            uploader = info.get('uploader', self.t('unknown_channel'))
            duration = info.get('duration')
            duration_str = f"{int(duration) // 60} {self.t('min')} {int(duration) % 60} {self.t('sec')}" if duration else self.t('unknown_duration')

        preview_card = self._card(parent=self.preview_container)
        preview_card.pack(fill="x")
        
        header = ctk.CTkFrame(preview_card, fg_color="transparent")
        header.pack(fill="x", padx=self.PADDING, pady=(10, 6))
        ctk.CTkLabel(header, text=self.t('preview_label'), font=self.FONT_SMALL, text_color="#4CAF50").pack(side="left")
        
        content_row = ctk.CTkFrame(preview_card, fg_color="transparent")
        content_row.pack(fill="x", padx=self.PADDING, pady=(0, 10))
        
        tw, th = self.THUMB_SIZE
        self.thumb_label = ctk.CTkLabel(content_row, text=self.t('img_loading'), width=tw, height=th, font=self.FONT_TINY)
        self.thumb_label.pack(side="left", padx=(0, 12))
        
        text_frame = ctk.CTkFrame(content_row, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)
        
        wrap_len = 350 if self.is_small_screen else 500
        title_font = self.FONT_TEXT if self.is_small_screen else self.FONT_LABEL
        ctk.CTkLabel(text_frame, text=title, font=title_font, anchor="w", justify="left", wraplength=wrap_len).pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(text_frame, text=f"{self.t('channel_label')} {uploader}", font=self.FONT_SMALL, text_color="gray", anchor="w", justify="left").pack(fill="x", pady=(0, 2))
        ctk.CTkLabel(text_frame, text=f"{self.t('duration_label')} {duration_str}", font=self.FONT_SMALL, text_color="gray", anchor="w", justify="left").pack(fill="x")

        if self.last_thumbnail_image is not None:
            self.thumb_label.configure(image=self.last_thumbnail_image, text="")
        else:
            thumbnail_url = self._get_thumbnail_url(info)
            if thumbnail_url:
                threading.Thread(target=self._fetch_thumbnail, args=(thumbnail_url, self.preview_request_id, self.last_preview_url), daemon=True).start()
            else:
                self.thumb_label.configure(text=self.t('no_image'))

    def _on_url_change(self, *args):
        url = self.url_var.get().strip()
        self.preview_request_id += 1
        if self.preview_after_id is not None:
            try: self.after_cancel(self.preview_after_id)
            except Exception: pass
            self.preview_after_id = None
        self.last_preview_info = None
        self.last_preview_url = None
        self.last_thumbnail_image = None
        if self.current_page != "download": return
        if not url:
            self._clear_preview()
            self._hide_download_button()
            self.status_var.set(self.t('status_ready'))
            return
        self._hide_download_button()
        if valid_url(url):
            request_id = self.preview_request_id
            self.preview_after_id = self.after(self.preview_debounce_ms, lambda u=url, rid=request_id: self._auto_fetch_preview(u, rid))
        else:
            self._clear_preview()

    def _auto_fetch_preview(self, url=None, request_id=None):
        if self.current_page != "download": return
        url = (url or self.url_var.get()).strip()
        request_id = self.preview_request_id if request_id is None else request_id
        if request_id != self.preview_request_id or url != self.url_var.get().strip(): return
        if not valid_url(url):
            self._clear_preview()
            self._hide_download_button()
            return
        self.preview_after_id = None
        self.status_var.set(self.t('status_fetching'))
        self._show_loading_preview()
        threading.Thread(target=self._preview_worker, args=(url, request_id, bool(self.playlist_var.get())), daemon=True).start()

    def _clear_preview(self):
        if self.preview_container is not None:
            try:
                if self.preview_container.winfo_exists(): self.preview_container.destroy()
            except Exception: pass
        self.preview_container = None
        self.thumb_label = None

    def _show_loading_preview(self):
        self._clear_preview()
        if self.current_page != "download" or not hasattr(self, "action_row"): return
        self.preview_container = ctk.CTkFrame(self.content, fg_color="transparent")
        self.preview_container.pack(fill="x", pady=(0, 10), before=self.action_row)
        loading_card = self._card(parent=self.preview_container)
        loading_card.pack(fill="x")
        ctk.CTkLabel(loading_card, text=self.t('loading_preview'), font=self.FONT_TEXT, text_color="gray").pack(pady=15)

    def _preview_worker(self, url, request_id, include_playlist):
        try:
            ydl_opts = {"quiet": True, "no_warnings": True, "noplaylist": not include_playlist, "playlistend": 1, "socket_timeout": 15, "retries": 2, "extractor_retries": 2}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            self.events.put(("preview_ready", (request_id, url, info)))
        except Exception as exc:
            self.events.put(("preview_error", (request_id, url, clean_error(exc))))

    @staticmethod
    def _get_thumbnail_url(info):
        thumbnail_url = info.get("thumbnail")
        if thumbnail_url: return thumbnail_url
        thumbnails = info.get("thumbnails") or []
        for thumbnail in reversed(thumbnails):
            if isinstance(thumbnail, dict) and thumbnail.get("url"): return thumbnail["url"]
        entries = info.get("entries")
        if entries:
            first_entry = next((entry for entry in entries if entry), None)
            if first_entry: return MultimediaDownloader._get_thumbnail_url(first_entry)
        return None

    def _show_preview(self, info, url, request_id):
        if request_id != self.preview_request_id or self.current_page != "download" or url != self.url_var.get().strip(): return
        self.last_preview_info = info
        self.last_preview_url = url
        self.last_thumbnail_image = None
        self._clear_preview()
        self.preview_container = ctk.CTkFrame(self.content, fg_color="transparent")
        self.preview_container.pack(fill="x", pady=(0, 10), before=self.action_row)

        is_playlist = info.get("_type") in ("playlist", "multi_video")
        if is_playlist:
            title = info.get("title") or self.t('playlist_title')
            count_text = str(info.get("playlist_count")) if info.get("playlist_count") else self.t('various')
            uploader = f"{info.get('uploader') or self.t('unknown_channel')} · {count_text} {self.t('playlist_elements')}"
            duration_str = self.t('playlist_title')
        else:
            title = info.get("title") or self.t('unknown_title')
            uploader = info.get("uploader") or info.get("channel") or self.t('unknown_channel')
            duration = info.get("duration")
            duration_str = f"{int(duration) // 60} {self.t('min')} {int(duration) % 60} {self.t('sec')}" if duration else self.t('unknown_duration')

        thumbnail_url = self._get_thumbnail_url(info)
        preview_card = self._card(parent=self.preview_container)
        preview_card.pack(fill="x")

        header = ctk.CTkFrame(preview_card, fg_color="transparent")
        header.pack(fill="x", padx=self.PADDING, pady=(10, 6))
        ctk.CTkLabel(header, text=self.t('preview_label'), font=self.FONT_SMALL, text_color="#4CAF50").pack(side="left")

        content_row = ctk.CTkFrame(preview_card, fg_color="transparent")
        content_row.pack(fill="x", padx=self.PADDING, pady=(0, 10))

        tw, th = self.THUMB_SIZE
        self.thumb_label = ctk.CTkLabel(content_row, text=self.t('img_loading') if thumbnail_url else self.t('no_image'), width=tw, height=th, font=self.FONT_TINY)
        self.thumb_label.pack(side="left", padx=(0, 12))

        text_frame = ctk.CTkFrame(content_row, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)

        wrap_len = 350 if self.is_small_screen else 500
        title_font = self.FONT_TEXT if self.is_small_screen else self.FONT_LABEL
        ctk.CTkLabel(text_frame, text=title, font=title_font, anchor="w", justify="left", wraplength=wrap_len).pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(text_frame, text=f"{self.t('channel_label')} {uploader}", font=self.FONT_SMALL, text_color="gray", anchor="w", justify="left").pack(fill="x", pady=(0, 2))
        ctk.CTkLabel(text_frame, text=f"{self.t('duration_label')} {duration_str}", font=self.FONT_SMALL, text_color="gray", anchor="w", justify="left").pack(fill="x")

        self.status_var.set(self.t('status_ready'))
        if not self.download_button.winfo_ismapped():
            self.download_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        if thumbnail_url:
            threading.Thread(target=self._fetch_thumbnail, args=(thumbnail_url, request_id, url), daemon=True).start()

    def _fetch_thumbnail(self, url, request_id, video_url):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
            with urllib.request.urlopen(request, timeout=15) as response:
                image_data = response.read()
            with Image.open(io.BytesIO(image_data)) as source_image:
                image = source_image.convert("RGB")
                image.thumbnail(self.THUMB_SIZE, Image.Resampling.LANCZOS)
            self.events.put(("thumbnail_ready", (request_id, video_url, image)))
        except Exception as exc:
            self.events.put(("thumbnail_error", (request_id, video_url, str(exc))))

    def _hide_download_button(self):
        if hasattr(self, "download_button"):
            try:
                if self.download_button.winfo_exists() and self.download_button.winfo_ismapped():
                    self.download_button.pack_forget()
            except Exception: pass

    def paste_url(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except Exception:
            messagebox.showinfo(self.t('msg_clipboard'), self.t('msg_clipboard_text'))

    def choose_folder(self):
        selected = filedialog.askdirectory(title=self.t('default_folder'), initialdir=self.folder_var.get() or str(Path.home()))
        if selected:
            self.folder_var.set(selected)
            self.save_settings()

    def open_download_folder(self):
        folder = Path(self.folder_var.get()).expanduser()
        folder.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32": os.startfile(str(folder))
        elif sys.platform == "darwin": subprocess.Popen(["open", str(folder)])
        else: subprocess.Popen(["xdg-open", str(folder)])

    def _make_ydl_options(self, url):
        folder = Path(self.folder_var.get()).expanduser()
        folder.mkdir(parents=True, exist_ok=True)
        quality = self.quality_var.get()

        if quality == self.t('quality_4k'): fmt = "bv*[height<=2160]+ba/b[height<=2160]/best"
        elif quality == self.t('quality_1080'): fmt = "bv*[height<=1080]+ba/b[height<=1080]/best"
        elif quality == self.t('quality_720'): fmt = "bv*[height<=720]+ba/b[height<=720]/best"
        elif quality in (self.t('quality_mp3'), self.t('quality_m4a')): fmt = "bestaudio/best"
        else: fmt = "bv*+ba/best"

        opts = {"format": fmt, "outtmpl": str(folder / "%(title).180B [%(id)s].%(ext)s"), "noplaylist": not self.playlist_var.get(), "ignoreerrors": False, "retries": 3, "fragment_retries": 3, "continuedl": True, "windowsfilenames": True, "progress_hooks": [self._progress_hook], "quiet": True, "no_warnings": False}

        if quality == self.t('quality_mp3'):
            opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
        elif quality == self.t('quality_m4a'):
            opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}]

        browser = self.cookies_var.get()
        if browser and browser != self.t('cookies_none'):
            opts["cookiesfrombrowser"] = (browser.lower(),)
        return opts

    def start_download(self):
        url = self.url_var.get().strip()
        if not valid_url(url):
            messagebox.showwarning(self.t('msg_invalid_url'), self.t('msg_invalid_url_text'))
            return
        if self.active_download:
            messagebox.showinfo(self.t('msg_downloading'), self.t('msg_downloading_text'))
            return
        self.save_settings()
        self.active_download = True
        self.download_button.configure(state="disabled", text=self.t('dl_btn_downloading'))
        self.progress_bar.set(0)
        self.progress_percent.configure(text="0%")
        self.status_var.set(self.t('status_preparing'))
        self.add_history(url, self.t('status_progress'), self.t('history_initiated'))
        self.download_thread = threading.Thread(target=self._download_worker, args=(url,), daemon=True)
        self.download_thread.start()

    def _download_worker(self, url):
        try:
            with yt_dlp.YoutubeDL(self._make_ydl_options(url)) as ydl:
                ydl.download([url])
            self.events.put(("download_finished", (url, True, self.t('history_completed'))))
        except Exception as exc:
            self.events.put(("download_finished", (url, False, clean_error(exc))))

    def _progress_hook(self, data):
        status = data.get("status")
        if status == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes", 0)
            percent = (downloaded / total * 100) if total else 0
            speed = data.get("speed")
            eta = data.get("eta")
            self.events.put(("progress", (percent, speed, eta)))
        elif status == "finished":
            self.events.put(("status", self.t('status_processing')))

    # ---------------------- ACTIVITY PAGE ----------------------
    def _build_activity_page(self):
        self._heading(self.t('act_title'), self.t('act_subtitle'))
        toolbar = ctk.CTkFrame(self.content, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(toolbar, text=f"{len(self.history)} {self.t('records_saved')}", text_color="gray", font=self.FONT_SMALL).pack(side="left")
        ctk.CTkButton(toolbar, text=self.t('update_btn'), width=100, height=self.BUTTON_HEIGHT, command=self._refresh_activity).pack(side="right", padx=(8, 0))
        ctk.CTkButton(toolbar, text=self.t('clear_hist_btn'), width=120, height=self.BUTTON_HEIGHT, fg_color="#8E3434", hover_color="#A64242", command=self.clear_history).pack(side="right")

        self.activity_list = ctk.CTkFrame(self.content, corner_radius=10, fg_color=("gray90", "gray13"))
        self.activity_list.pack(fill="x", pady=(0, 15))
        self.after(100, self._refresh_activity)

    def _refresh_activity(self):
        if not hasattr(self, "activity_list") or not self.activity_list.winfo_exists(): return
        for child in self.activity_list.winfo_children(): child.destroy()
        if not self.history:
            ctk.CTkLabel(self.activity_list, text=self.t('no_records'), text_color="gray", justify="center", font=self.FONT_TEXT).pack(pady=40, padx=20)
            return
        for item in self.history:
            card = ctk.CTkFrame(self.activity_list, corner_radius=8)
            card.pack(fill="x", padx=10, pady=4)
            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(8, 2))
            status = item.get("status", self.t('status_unknown'))
            color = "#35A66F" if status == self.t('status_completed') else ("#C58A35" if status == self.t('status_progress') else "#C45B5B")
            ctk.CTkLabel(top, text=status, text_color=color, font=self.FONT_SMALL).pack(side="left")
            ctk.CTkLabel(top, text=item.get("date", ""), text_color="gray", font=self.FONT_TINY).pack(side="right")
            wrap_len = 400 if self.is_small_screen else 600
            ctk.CTkLabel(card, text=item.get("url", ""), anchor="w", justify="left", wraplength=wrap_len, font=self.FONT_SMALL).pack(fill="x", padx=10, pady=(2, 2))
            detail = item.get("details", "")
            if detail:
                ctk.CTkLabel(card, text=detail, anchor="w", justify="left", wraplength=wrap_len, text_color="gray", font=self.FONT_TINY).pack(fill="x", padx=10, pady=(0, 8))

    def clear_history(self):
        if not self.history: return
        if messagebox.askyesno(self.t('msg_clear_hist'), self.t('msg_clear_hist_text')):
            self.history.clear()
            safe_write_json(HISTORY_FILE, self.history)
            self._refresh_activity()

    # ---------------------- SETTINGS PAGE ----------------------
    def _build_settings_page(self):
        self._heading(self.t('settings_title'), self.t('settings_subtitle'))
        appearance = self._card()
        appearance.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(appearance, text=self.t('appearance_label'), font=self.FONT_LABEL, text_color="gray").pack(anchor="w", padx=self.PADDING, pady=(12, 6))
        row = ctk.CTkFrame(appearance, fg_color="transparent")
        row.pack(fill="x", padx=self.PADDING, pady=(0, 12))
        ctk.CTkLabel(row, text=self.t('theme_label'), font=self.FONT_TEXT).pack(side="left")
        ctk.CTkSegmentedButton(row, values=[self.t('theme_dark'), self.t('theme_light'), self.t('theme_system')], variable=self.theme_var, command=self.change_theme, height=self.BUTTON_HEIGHT).pack(side="right")

        lang_row = ctk.CTkFrame(appearance, fg_color="transparent")
        lang_row.pack(fill="x", padx=self.PADDING, pady=(0, 12))
        ctk.CTkLabel(lang_row, text=self.t('lang_label'), font=self.FONT_TEXT).pack(side="left")
        ctk.CTkSegmentedButton(lang_row, values=[self.t('lang_es'), self.t('lang_en')], variable=ctk.StringVar(value=self.t('lang_es') if self.lang == 'es' else self.t('lang_en')), command=self.change_language, height=self.BUTTON_HEIGHT).pack(side="right")

        downloads = self._card()
        downloads.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(downloads, text=self.t('downloads_label'), font=self.FONT_LABEL, text_color="gray").pack(anchor="w", padx=self.PADDING, pady=(12, 6))
        ctk.CTkLabel(downloads, text=self.t('default_folder'), font=self.FONT_TEXT).pack(anchor="w", padx=self.PADDING)
        folder_row = ctk.CTkFrame(downloads, fg_color="transparent")
        folder_row.pack(fill="x", padx=self.PADDING, pady=(4, 10))
        ctk.CTkEntry(folder_row, textvariable=self.folder_var, height=self.ENTRY_HEIGHT).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(folder_row, text=self.t('change_btn'), width=90, height=self.ENTRY_HEIGHT, command=self.choose_folder).pack(side="right")
        
        ctk.CTkLabel(downloads, text=self.t('default_quality'), font=self.FONT_TEXT).pack(anchor="w", padx=self.PADDING)
        ctk.CTkComboBox(downloads, variable=self.quality_var, state="readonly", values=self.get_quality_values(), height=self.ENTRY_HEIGHT).pack(anchor="w", fill="x", padx=self.PADDING, pady=(4, 10))
        ctk.CTkCheckBox(downloads, text=self.t('playlist_default'), variable=self.playlist_var).pack(anchor="w", padx=self.PADDING, pady=(0, 12))

        privacy = self._card()
        privacy.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(privacy, text=self.t('privacy_label'), font=self.FONT_LABEL, text_color="gray").pack(anchor="w", padx=self.PADDING, pady=(12, 6))
        ctk.CTkLabel(privacy, text=self.t('cookies_text'), font=self.FONT_TEXT).pack(anchor="w", padx=self.PADDING)
        ctk.CTkComboBox(privacy, variable=self.cookies_var, state="readonly", values=self.get_cookies_values(), height=self.ENTRY_HEIGHT).pack(anchor="w", fill="x", padx=self.PADDING, pady=(4, 12))

        buttons = ctk.CTkFrame(self.content, fg_color="transparent")
        buttons.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(buttons, text=self.t('save_btn'), height=self.BUTTON_HEIGHT, command=self.save_settings).pack(side="left")
        ctk.CTkButton(buttons, text=self.t('reset_btn'), height=self.BUTTON_HEIGHT, fg_color=("gray75", "gray25"), text_color=("gray10", "white"), command=self.reset_settings).pack(side="left", padx=9)
        
        wrap_len = 500 if self.is_small_screen else 700
        ctk.CTkLabel(self.content, text=f"{self.t('config_path')} {CONFIG_FILE}", text_color="gray", font=self.FONT_TINY, wraplength=wrap_len).pack(anchor="w", pady=(10, 15))

    def change_theme(self, value):
        theme_map = {self.t('theme_dark'): "Dark", self.t('theme_light'): "Light", self.t('theme_system'): "System"}
        ctk.set_appearance_mode(theme_map.get(value, value))
        self.save_settings()

    def change_language(self, value):
        lang_map = {self.t('lang_es'): "es", self.t('lang_en'): "en"}
        new_lang = lang_map.get(value, self.lang)
        if new_lang != self.lang:
            self.lang = new_lang
            self.save_settings()
            if hasattr(self, 'lbl_sidebar_title'): self.lbl_sidebar_title.configure(text=self.t('sidebar_title'))
            if hasattr(self, 'lbl_sidebar_subtitle'): self.lbl_sidebar_subtitle.configure(text=f"{self.t('sidebar_subtitle')} · v{APP_VERSION}")
            if hasattr(self, 'lbl_sys_status'): self.lbl_sys_status.configure(text=self.t('sys_status'))
            if hasattr(self, 'dependencies_label') and self.dependencies_label.winfo_exists(): self._update_dependencies_label()
            if hasattr(self, 'donate_button'): self.donate_button.configure(text=self.t('donate_btn'))
            if hasattr(self, 'lbl_disclaimer'): self.lbl_disclaimer.configure(text=self.t('disclaimer'))
            for key, button in self.nav_buttons.items():
                if key == 'download': button.configure(text=self.t('nav_download'))
                elif key == 'activity': button.configure(text=self.t('nav_activity'))
                elif key == 'settings': button.configure(text=self.t('nav_settings'))
            if not self.active_download:
                self.status_var.set(self.t('status_ready'))
                if hasattr(self, 'download_button') and self.download_button.winfo_exists():
                    self.download_button.configure(text=self.t('dl_btn'))
            self.show_page(self.current_page)

    def reset_settings(self):
        if not messagebox.askyesno(self.t('msg_reset'), self.t('msg_reset_text')): return
        self.folder_var.set(str(DEFAULT_DOWNLOAD_DIR))
        self.quality_var.set(self.t('quality_best'))
        self.cookies_var.set(self.t('cookies_none'))
        self.playlist_var.set(False)
        self.theme_var.set(self.t('theme_dark'))
        self.lang = "es"
        ctk.set_appearance_mode("Dark")
        self.save_settings()
        self.show_page("settings")

    # ---------------------- EVENTS / STATUS ----------------------
    def _process_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "progress":
                    percent, speed, eta = payload
                    self.progress_var.set(percent / 100)
                    if hasattr(self, "progress_bar") and self.progress_bar.winfo_exists():
                        self.progress_bar.set(percent / 100)
                        self.progress_percent.configure(text=f"{percent:.1f}%")
                    speed_text = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "—"
                    eta_text = f"{eta}s" if eta is not None else "—"
                    self.status_var.set(f"{self.t('status_downloading')} · {speed_text} · ETA {eta_text}")
                elif event == "status":
                    self.status_var.set(payload)
                elif event == "download_finished":
                    url, success, details = payload
                    self.active_download = False
                    state = self.t('status_completed') if success else self.t('status_error')
                    self.add_history(url, state, details)
                    if self.current_page == "download" and hasattr(self, "download_button"):
                        try: self.download_button.configure(state="normal", text=self.t('dl_btn'))
                        except Exception: pass
                        self.status_var.set(self.t('history_completed') if success else self.t('history_error'))
                        if success:
                            self.progress_bar.set(1)
                            self.progress_percent.configure(text="100%")
                    if success: messagebox.showinfo(self.t('msg_completed'), details)
                    else: messagebox.showerror(self.t('msg_error'), details)
                elif event == "history_changed" and self.current_page == "activity":
                    self._refresh_activity()
                elif event == "preview_ready":
                    request_id, url, info = payload
                    self._show_preview(info, url, request_id)
                elif event == "preview_error":
                    request_id, url, error = payload
                    if request_id == self.preview_request_id and self.current_page == "download" and url == self.url_var.get().strip():
                        self._clear_preview()
                        self._hide_download_button()
                        self.status_var.set(self.t('status_failed_preview'))
                elif event == "thumbnail_ready":
                    request_id, url, image = payload
                    if request_id == self.preview_request_id and self.current_page == "download" and url == self.url_var.get().strip() and self.thumb_label is not None:
                        try:
                            if self.thumb_label.winfo_exists():
                                tw, th = self.THUMB_SIZE
                                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(tw, th))
                                self.last_thumbnail_image = ctk_image
                                self.thumb_label.configure(image=ctk_image, text="")
                        except Exception: pass
                elif event == "thumbnail_error":
                    request_id, url, error = payload
                    if request_id == self.preview_request_id and self.current_page == "download" and url == self.url_var.get().strip() and self.thumb_label is not None:
                        try:
                            if self.thumb_label.winfo_exists(): self.thumb_label.configure(text=self.t('img_error'))
                        except Exception: pass
        except queue.Empty:
            pass
        self.after(120, self._process_events)

    def _check_dependencies(self):
        self._update_dependencies_label()

    def _update_dependencies_label(self):
        if not hasattr(self, 'dependencies_label') or not self.dependencies_label.winfo_exists(): return
        ffmpeg = shutil.which("ffmpeg")
        deno = shutil.which("deno")
        lines = [f"FFmpeg: {self.t('ffmpeg_avail') if ffmpeg else self.t('ffmpeg_not')}", f"Deno: {self.t('deno_avail') if deno else self.t('deno_opt')}"]
        self.dependencies_label.configure(text="\n".join(lines))

    def open_donation(self):
        webbrowser.open("https://mariosandovalp3.github.io/donaciones/")

def clean_error(exc):
    text = str(exc).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > 900: text = text[:900] + "…"
    return text or "Error desconocido durante la descarga."

if __name__ == "__main__":
    try:
        app = MultimediaDownloader()
        app.mainloop()
    except Exception as e:
        print(f"\n[ERROR CRÍTICO EN LA APLICACIÓN]: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para cerrar esta ventana...")