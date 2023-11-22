import sys

from cx_Freeze import Executable, setup

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["plugins"],
                    excludes = [], include_files = [])


base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pyautokey.py', base=base, targetName='pyautokey')
]

setup(name='pyautokey',
      version = '1.0',
      description = 'pyautokey',
      options = dict(build_exe = buildOptions),
      executables = executables)