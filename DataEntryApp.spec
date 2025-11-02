# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Add all data files
added_files = [
    ('agent_suggestions.json', '.'),
    ('city_suggestions.json', '.'),
    ('mkt_committee_suggestions.json', '.'),
    ('party_name_suggestions.json', '.'),
    ('formulas.json', '.'),
    ('maize_project/maize app/yellow.ico', 'maize_project/maize app')
]

# Collect all required packages
datas = []
binaries = []
hiddenimports = []

# Add required packages
def collect_package_data(package_name):
    try:
        pkg_data, pkg_binaries, pkg_hidden = collect_all(package_name)
        return pkg_data, pkg_binaries, pkg_hidden
    except Exception as e:
        print(f"Warning: Could not collect all data for {package_name}: {str(e)}")
        return [], [], []

# Collect openpyxl data
openpyxl_data, openpyxl_binaries, openpyxl_hidden = collect_package_data('openpyxl')
datas.extend(openpyxl_data)
binaries.extend(openpyxl_binaries)
hiddenimports.extend(openpyxl_hidden)

# Collect numpy data (excluding tests)
numpy_data, numpy_binaries, numpy_hidden = collect_package_data('numpy')
datas.extend([d for d in numpy_data if 'tests' not in d[0]])
binaries.extend([b for b in numpy_binaries if 'tests' not in b[0]])
hiddenimports.extend([h for h in numpy_hidden if 'tests' not in h])

# Add necessary numpy core modules
numpy_core_modules = [
    'numpy.core._methods',
    'numpy.core._multiarray_umath',
    'numpy.core.numeric',
    'numpy.core.fromnumeric',
    'numpy.core._asarray',
    'numpy.core._dtype',
    'numpy.core._type_aliases',
    'numpy.core._string_helpers',
    'numpy.core._exceptions'
]

# Add numpy submodules
hiddenimports.extend([
    'numpy',
    'numpy.core',
    'numpy.core.numeric',
    'numpy.core.multiarray',
    'numpy.core.umath',
    'numpy.core.fromnumeric',
    'numpy.lib',
    'numpy.lib.npyio',
    'numpy.linalg',
    'numpy.random'
])

hiddenimports.extend(numpy_core_modules)

# Add other necessary imports
hiddenimports.extend([
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    '_tkinter',
    'json',
    'os',
    'sys',
    'datetime',
    'logging',
    'traceback',
    'collections.abc',
    'collections',
    'openpyxl.cell',
    'openpyxl.styles',
    'openpyxl.utils',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.xml',
    'openpyxl.xml.functions',
    'openpyxl.reader.excel',
    'openpyxl.writer.excel',
    'xml.etree',
    'xml.etree.ElementTree'
])

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath(SPECPATH)],
    binaries=binaries,
    datas=datas + added_files,
    hiddenimports=list(set(hiddenimports)),  # Remove duplicates
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'PyQt5', 'PySide2', 'PIL'],  # Exclude unnecessary large packages
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DataEntryApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='maize_project/maize app/yellow.ico'
)