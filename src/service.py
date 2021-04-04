from os import environ, listdir
from database import Files
from tempfile import mkstemp, mkdtemp
from pathlib import Path
from typing import Optional, List, TypedDict

from download import download
from zip import unzip
from aws import S3Manager

import pandas as pd

PGFN_DEFAULT_URL = 'http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip'
BACEN_DEFAULT_URL = ''

class Info(TypedDict):
    path: str
    files: List[str]

class DataCrawlerInterface:
    def download(self) -> str:
        raise Exception('Not Implemented yet')

    def unzip(self, cod: str) -> str:
        raise Exception('Not Implemented yet')

    def prepare(self, cod: str) -> str:
        raise Exception('Not Implemented yet')

    def send(self, cod: str) -> str:
        raise Exception('Not Implemented yet')

    @staticmethod
    def info(cod: str, kind: Optional[str] = None) -> Info:
        path = Path(Files.get_path_from_cod(cod))
        if path.is_dir():
            return { "path": str(path), "files": [f for f in listdir(path) if Path(Path(path) / f).is_file()]}
        else:
            return {"path": str(path), "files": []}


class PGFN(DataCrawlerInterface):

    def download(self) -> str:
        url_pgfn = environ[
            'URL_ARQUIVO_PGFN'] if 'URL_ARQUIVO_PGFN' in environ else PGFN_DEFAULT_URL
        file_was_downloaded = Files.exists_file(url_pgfn)
        if file_was_downloaded is not None:
            return file_was_downloaded
        _, temp_file_name = mkstemp(suffix='.zip')
        download(url_pgfn, file_name=temp_file_name)
        f = Files().new(temp_file_name, url_pgfn)
        f.save()
        return f.cod

    def unzip(self, file_path: str) -> tuple[str, list]:
        tempdir = mkdtemp()
        fp = Files.get_from_source(file_path, kind='unzipe-files-dir')
        if fp is None:
            data_files = unzip(file_path, out=tempdir)
            fp = Files()
            fp.new(path=tempdir, source=file_path, kind='unzipe-files-dir')
            fp.save()
        else:
            tempdir = fp.path
            data_files = [f for f in listdir(tempdir) if Path(Path(tempdir) / f).is_file()]
        return fp.cod, [Path(tempdir) / file for file in data_files]

    def __join(self, all_files: list) -> pd.DataFrame:
        try:
            return pd.concat((pd.read_csv(f, sep=';', encoding='ANSI') for f in all_files), ignore_index=True)
        except LookupError:
            return pd.concat((pd.read_csv(f, sep=';', encoding='ISO-8859-1') for f in all_files), ignore_index=True)

    def __clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # transform text column in True/False column
        df["INDICADOR_AJUIZADO"] = df["INDICADOR_AJUIZADO"] == 'SIM'
        df['PESSOA_FISICA'] = df['TIPO_PESSOA'] == 'Pessoa física'
        df['DEVEDOR_PRINCIPAL'] = df['TIPO_DEVEDOR'] == 'PRINCIPAL'

        # remove column
        df.drop('TIPO_PESSOA', inplace=True, axis=1)
        df.drop('TIPO_DEVEDOR', inplace=True, axis=1)
        df.drop('NOME_DEVEDOR', inplace=True, axis=1)
        df.drop('CPF_CNPJ', inplace=True, axis=1)
        df.drop('UNIDADE_RESPONSAVEL', inplace=True, axis=1)
        df.drop('RECEITA_PRINCIPAL', inplace=True, axis=1)

        return df

    def __make_files(self, df: pd.DataFrame) -> str:
        tempdir = mkdtemp()

        # split dataframe in diverse csv files
        df[df['PESSOA_FISICA']].to_csv(Path(tempdir) / 'pessoa_fisica.csv', encoding='utf8', index_label='line')
        df[~df['PESSOA_FISICA']].to_csv(Path(tempdir) / 'pessoa_juridica.csv', encoding='utf8', index_label='line')
        df[df['DEVEDOR_PRINCIPAL']].to_csv(Path(tempdir) / 'devedor_principal.csv', encoding='utf8', index_label='line')
        df[~df['DEVEDOR_PRINCIPAL']].to_csv(Path(tempdir) / 'devedor_corresponsavel.csv', encoding='utf8',
                                            index_label='line')
        df[df['INDICADOR_AJUIZADO']].to_csv(Path(tempdir) / 'acao_ajuizada.csv', encoding='utf8', index_label='line')
        df[~df['INDICADOR_AJUIZADO']].to_csv(Path(tempdir) / 'acao_nao_ajuizada.csv', encoding='utf8',
                                             index_label='line')
        return tempdir

    def prepare(self, cod: str) -> str:
        file_path = Files.get_path_from_cod(cod)
        unziped_dir_cod, files = self.unzip(file_path)
        f = Files.get_from_source(cod, kind='prepared-files-dir')
        if f is None:
            tempdir = self.__make_files(self.__clean_data(self.__join(files)))
            f = Files()
            f.new(path=tempdir, source=cod, kind='prepared-files-dir')
            f.save()
        return f.cod

    def send(self, cod: str) -> str:
        s3 = S3Manager()
        if s3.connect():
            file_path = Files.get_path_from_cod(cod)
            for f in listdir(file_path):
                s3.upload_file(path=file_path, file_name=f)
        return 'done'

class Bacen(DataCrawlerInterface):
    def download(self) -> str:
        return 'Não Implementado'

    def unzip(self, cod: str) -> str:
        return 'Não Implementado'

    def prepare(self, cod: str) -> str:
        return 'Não Implementado'

    def send(self, cod: str) -> str:
        return 'Não Implementado'
