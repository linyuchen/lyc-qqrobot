import configparser
import subprocess
from pathlib import Path


def re_write_config(ini_path: Path, db_path: Path) -> Path:
    """
    return new config path
    """
    config = configparser.ConfigParser()
    config.read(ini_path)
    config['alembic']['sqlalchemy.url'] = f'sqlite:///{db_path}'
    config['alembic']['script_location'] = str(Path(ini_path).parent / 'alembic')
    new_file_name = 'new.' + ini_path.name
    new_path = ini_path.parent / new_file_name
    with open(new_path, 'w') as f:
        config.write(f)
    return new_path


def upgrade(ini_path: Path):
    result = subprocess.run(['alembic', '-c', ini_path, 'upgrade', 'head'])
    print(result)


def gen_migration(ini_path: Path):
    result = subprocess.run(['alembic', '-c', ini_path, 'revision', '--autogenerate'])
    print(result)
