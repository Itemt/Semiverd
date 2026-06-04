# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

import face_recognition_models
face_recognition_models_path = os.path.dirname(face_recognition_models.__file__)

# Archivos estáticos a incluir dentro del binario
added_files = [
    ('views', 'views'),
    (os.path.join(face_recognition_models_path, 'models'), 'face_recognition_models/models'),
]

# Hidden imports comunes a ambas plataformas
common_hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan.on',
    'uvicorn.lifespan.off',
    'models.models',
    'models.schemas',
    'face_recognition',
    'passlib.handlers.bcrypt',
    'bcrypt',
    # pywebview - núcleo
    'webview',
    'webview.platforms',
    'webview.window',
    'webview.guilib',
    'webview.util',
    'webview.http',
    'webview.event',
    # Soporte JSON / serialización
    'json',
    'urllib.request',
]

# Hidden imports específicos de Windows (WebView2 / win32)
windows_hidden_imports = [
    'clr',
    'pythoncom',
    'win32api',
    'win32con',
    'webview.platforms.winforms',
    'webview.platforms.edgechromium',
    'webview.platforms.mshtml',
    'System',
    'System.Windows.Forms',
    'System.Drawing',
]

# Hidden imports específicos de macOS (WebKit / Cocoa + PostgreSQL)
macos_hidden_imports = [
    'webview.platforms.cocoa',
    'webview.platforms.gtk',
    'psycopg2',  # Solo macOS: en Windows usamos SQLite
]

if sys.platform == 'win32':
    platform_hidden_imports = windows_hidden_imports
else:
    platform_hidden_imports = macos_hidden_imports

all_hidden_imports = common_hidden_imports + platform_hidden_imports

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=all_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Agregar los datos de pywebview (plantillas HTML internas, etc.)
try:
    import webview
    webview_path = os.path.dirname(webview.__file__)
    # Incluir todos los assets del paquete pywebview
    for root, dirs, files in os.walk(webview_path):
        for f in files:
            full = os.path.join(root, f)
            rel  = os.path.relpath(full, os.path.dirname(webview_path))
            a.datas.append((rel, full, 'DATA'))
except Exception as e:
    print(f"Advertencia: no se pudieron incluir los datos de pywebview: {e}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if sys.platform == 'darwin':
    # macOS: Generar un .app bundle (directorio distribuido que se empaqueta en .dmg)
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name='Semiverd',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,  # Sin ventana de consola en macOS
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='Semiverd',
    )
    
    app = BUNDLE(
        coll,
        name='Semiverd.app',
        icon='icon.ico',
        bundle_identifier='com.semiverd.app',
    )
else:
    # Windows: Generar un solo archivo ejecutable (.exe) portable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='Semiverd',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,         # ← Consola visible para diagnóstico en Windows
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
