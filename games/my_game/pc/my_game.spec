# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/var/folders/ht/1_5_x4r554n19n108zhw144c0000gn/T/.pyxel/app2exe/my_game.py'],
    pathex=[],
    binaries=[],
    datas=[('../my_game.pyxapp', '.')],
    hiddenimports=['pyxel'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='my_game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='my_game.app',
    icon=None,
    bundle_identifier=None,
)
