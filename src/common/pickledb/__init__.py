import pickle
from pathlib import Path
from typing import TypeVar, Generic

T = TypeVar('T')


class PickleDB(Generic[T]):
    def __init__(self, db_path: Path, init_data: T):
        self.db_path = db_path
        self.db_data: T = init_data
        self.read()

    def read(self) -> T:
        try:
            self.db_data = pickle.load(open(self.db_path, 'rb'))
        except Exception as e:
            print(f'load {self.db_path} failed, {e}, use default data')

        return self.db_data

    def save(self, data=None):
        if data:
            self.db_data = data
        try:
            pickle.dump(self.db_data, open(self.db_path, 'wb'))
        except Exception as e:
            print(f'save {self.db_path} failed', e)
