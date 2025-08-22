import sys, pathlib
# Ensure project root (where src/ lives) is on sys.path for imports
root = pathlib.Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
