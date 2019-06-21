# -*- mode: python -*-

block_cipher = None


a = Analysis(['dcs-hotas-kneeboard\\dcs-hotas-kneeboard.py'],
             pathex=['C:\\Users\\garre\\Documents\\Projects\\DCS-HOTAS-Kneeboard'],
             binaries=[],
             datas=[('dcs-hotas-kneeboard\\res\\*', 'res')],
             hiddenimports=[],
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
          name='dcs-hotas-kneeboard',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='dcs-hotas-kneeboard\\res\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dcs-hotas-kneeboard')