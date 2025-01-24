from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

DATA_DIR = BASE_DIR / "data"
PLAYWRIGHT_DATA_DIR = DATA_DIR / "playwright_chrome_data"
