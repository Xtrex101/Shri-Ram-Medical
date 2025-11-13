# -*- mode: python ; coding: utf-8 -*-
#
# NOTE: Ensure 'main.py', 'logo.png', and 'logo.ico' are in the same directory.
#
from PyInstaller.utils.hooks import collect_data_files

# 1. ANALYSIS: Defines the source and collects dependencies.
a = Analysis(
    # Assuming your main script is named 'main.py'
    ['main.py'],
    pathex=[],
    binaries=[],
    
    # CRITICAL FIX 1: Collect ReportLab resources for PDF generation.
    # CRITICAL FIX 2: Include your custom logo image.
    datas=collect_data_files('reportlab') + [('logo.png', '.')],
    
    # CRITICAL FIX 3: Add essential hidden imports for PyQt6 and ReportLab reliability.
    hiddenimports=['PyQt6.sip', 'reportlab.lib.list', 'PyQt6.QtPrintSupport'],
    
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# 2. PYZ: Bundles the Python modules and bytecode.
pyz = PYZ(a.pure)

# 3. EXE: Creates the final single-file executable.
exe = EXE(
    pyz,
    a.scripts,
    # PASS all collected binaries, zipfiles, and data directly to EXE:
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    
    name='SRM', # The name of the final executable file
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    
    # CRITICAL FIX 4: Set console=False for GUI application
    console=False, 
    
    # CRITICAL FIX 5: Add icon path (ensure 'logo.ico' exists)
    icon='logo.ico',
    
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# 4. COLLECT: This block is correctly REMOVED to force a single-file build. 
# Do not include the 'coll = COLLECT(...)' block.