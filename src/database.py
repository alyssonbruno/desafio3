from orator import DatabaseManager, Schema
from uuid import uuid4

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': 'dcstone.db',
    }
}

db = DatabaseManager(config)
schema = Schema(db)
class File:
    def __init__(self, nome):
        if not schema.has_table('files'):
            self.__create_table()

    def __create_table(self):
        with schema.create('files') as table:
            table.char('cod',16).unique()
            table.string('nome',255)
            table.primary('cod')