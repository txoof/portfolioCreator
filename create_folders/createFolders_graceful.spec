# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['createFolders_graceful.py'],
             pathex=['/Users/aaronciuffo/Documents/src/portfolioCreator/create_folders'],
             binaries=[],
             datas=[('logging_cfg.ini', '.'),
                    ('createFolders.ini', '.'),
                    ('HELP.md', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['IPython'],
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
          name='createFolders_graceful',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='createFolders_graceful')
