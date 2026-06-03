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

# No special append here, we will copy this manually in a post-build step

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
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
        'psycopg2',
        'face_recognition',
        'passlib.handlers.bcrypt',
    ],
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
        console=True,  # Mantener consola para visualizar logs de FastAPI
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
