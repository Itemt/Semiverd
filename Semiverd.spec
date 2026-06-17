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
    'json',
    'urllib.request',
]

# Hidden imports específicos de Windows
windows_hidden_imports = [
    'clr',
    'pythoncom',
    'win32api',
    'win32con',
]

# Hidden imports específicos de macOS (PostgreSQL)
macos_hidden_imports = [
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
        console=False,  # Sin ventana de consola en macOS (corre en background y abre navegador)
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
        runtime_tmpdir='%LOCALAPPDATA%\\Semiverd\\cache',
        console=True,         # Consola visible para diagnóstico en Windows
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
