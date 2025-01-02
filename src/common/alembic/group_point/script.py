from pathlib import Path
from functools import partial

from src.common.alembic.tool import upgrade, gen_migration, re_write_config
from src.common.group_point.models import db_path

cur_path = Path(__file__).parent
ini_path = cur_path / 'alembic.ini'


def upgrade_group_point_db():
    temp_ini_path = re_write_config(ini_path, db_path)
    gen_migration(temp_ini_path)
    upgrade(temp_ini_path)
    temp_ini_path.unlink()
