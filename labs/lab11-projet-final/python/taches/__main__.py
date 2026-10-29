import sys
from pathlib import Path

from taches.cli import main

code, sortie = main(sys.argv[1:], Path("taches.json"))
print(sortie)
sys.exit(code)
