from orator import DatabaseManager, Schema, Model

from typing import Optional
from uuid import uuid4
from pathlib import Path
from tempfile import gettempdir as tempdir

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': Path(tempdir())/'dcstone.db',
    }
}

db = DatabaseManager(config)
schema = Schema(db)
Model.set_connection_resolver(db)

def cria_schema() -> None:
    if not schema.has_table('files'):
        create_table_files()
    return None

def create_table_files() -> None:
    with schema.create('files') as table:
        table.char('cod',36).unique()
        table.string('path',255)
        table.string('source', 1024)
        table.string('kind', 30)
        table.datetime('created_at')
        table.datetime('updated_at')
        table.primary('cod')
        return None

class Files(Model):
    __table__ = 'files'
    __guarded__ = ['*']

    def __init__(self):
        super(Files, self).__init__()
        cria_schema()

    @staticmethod
    def exists_file(source: str) -> str:
        cria_schema()
        files = db.table('files').where('source', source).get()
        for f in files:
            p = Path(f['path'])
            if p.exists():
                return f['cod']
        return None

    @staticmethod
    def get_path_from_cod(cod: str) -> str:
        cria_schema()
        path_to_file = db.table('files').where('cod', cod).first()['path']
        return path_to_file

    @staticmethod
    def get_path_from_kind(kind: str) -> str:
        cria_schema()
        path_to_file = db.table('files').where('kind', kind).first()['path']
        return path_to_file

    @staticmethod
    def get_from_source(source: str, kind: Optional[str] = None) -> Optional[Model]:
        cria_schema()
        try:
            if kind is not None:
                path_to_file = db.table('files').where('source', source).where('kind',kind).first()
            else:
                path_to_file = db.table('files').where('source', source).first()
        except TypeError:
            return None
        return path_to_file

    def new(self, path : str, source: str, kind: Optional[str] = None) -> Model:
        self.cod = str(uuid4())
        self.path = path
        self.source = source if source is not None else 'local'
        self.kind = kind if kind is not None else 'file-downloaded'
        return self
