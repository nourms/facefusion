import subprocess
import sys
from textwrap import dedent

import pytest


@pytest.mark.parametrize('return_code', [ 0, 1, 2 ])
def test_install_exit_code(return_code : int) -> None:
	script = dedent('''
		import runpy
		import sys
		from unittest.mock import patch

		from facefusion import installer

		return_codes = [0] * len(installer.ONNXRUNTIME_SET) + [int(sys.argv[1])]
		sys.argv = [ 'install.py', 'default', '--skip-conda' ]

		with patch('facefusion.installer.shutil.which', return_value = 'pip'), \\
			patch('facefusion.installer.subprocess.call', side_effect = return_codes):
			runpy.run_path('install.py', run_name = '__main__')
	''')
	result = subprocess.run([ sys.executable, '-c', script, str(return_code) ], capture_output = True, text = True, timeout = 30)

	assert result.returncode == return_code, result.stdout + result.stderr
