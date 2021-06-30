# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['OSTU_Bin.py'],
             pathex=['D:\\HuahaoV2'],
             binaries=[],
             datas=[('./Earth.ico','./')],
             hiddenimports=[PyQt5.sip,win32com,],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='OSTU_Bin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='Earth.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OSTU_Bin')
