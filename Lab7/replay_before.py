"""Replay the original failures in a disposable directory."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='lab7-before-') as directory:
    target = Path(directory)
    shutil.copyfile(here / 'processor_before.txt', target / 'processor.py')
    shutil.copyfile(here / 'test_processor.py', target / 'test_processor.py')
    result = subprocess.run([sys.executable, '-m', 'pytest',
        '-p', 'hypothesis.extra.pytestplugin', 'test_processor.py', '-q',
        '--tb=short', '-k',
        'no_crash or compression_ratio_safe or bandwidth_tier_rate_safe'],
        cwd=target)
    print('Original application test exit code:', result.returncode)
    raise SystemExit(result.returncode)
