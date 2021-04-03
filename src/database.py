from orator import DatabaseManager, Schema, Model

from typing import Optional
from uuid import uuid4
from pathlib import Path

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': 'dcstone.db',
    }
}

db = DatabaseManager(config)
schema = Schema(db)
Model.set_connection_resolver(db)

class Files(Model):
    __table__ = 'files'
    __guarded__ = ['*']

    def __init__(self):
        super(Files, self).__init__()
        if not schema.has_table('files'):
            self.__create_table()

    @staticmethod
    def exists_file(url: str) -> str:
        files = db.table('files').where('url', url).get()
        for f in files:
            p = Path(f['nome'])
            if p.exists():
                return f['cod']
        return None

    def __create_table(self) -> None:
        with schema.create('files') as table:
            table.char('cod',36).unique()
            table.string('nome',255)
            table.string('url', 1024)
            table.datetime('created_at')
            table.datetime('updated_at')
            table.primary('cod')
            return None

    def new(self, nome : str, url: Optional[str] = None) -> Model:
        self.cod = str(uuid4())
        self.nome = nome
        self.url = url if url is not None else 'local'
        return self
