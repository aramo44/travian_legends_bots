import sys
import os

# Add the repo root and the selenium exploits directory to sys.path so modules
# can be imported in tests without installing them as packages.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELENIUM_DIR = os.path.join(REPO_ROOT, "selenium_UI based_exploits")

for p in (REPO_ROOT, SELENIUM_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
