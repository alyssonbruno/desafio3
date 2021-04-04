from os import environ
from database import Files
from tempfile import mkstemp, mkdtemp
from pathlib import Path

from download import download
from zip import unzip

import pandas as pd

PGFN_DEFAULT_URL = 'http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip'
BACEN_DEFAULT_URL = ''

class DataCrawlerInterface:
    def download(self) -> str:
        raise Exception('Not Implemented yet')

    def unzip(self, cod: str) -> str:
        raise Exception('Not Implemented yet')

class PGFN(DataCrawlerInterface):

    def download(self) -> str:
        url_pgfn = environ[
            'URL_ARQUIVO_PGFN'] if 'URL_ARQUIVO_PGFN' in environ else PGFN_DEFAULT_URL
        file_was_downloaded = Files.exists_file(url_pgfn)
        if file_was_downloaded is not None:
            return file_was_downloaded
        _, temp_file_name = mkstemp(suffix='.zip')
        download(url_pgfn,file_name=temp_file_name)
        f = Files().new(temp_file_name, url_pgfn)
        f.save()
        return f.cod

    def unzip(self, cod: str) -> tuple[str, list]:
        tempdir = mkdtemp()
        file_path = Files.get_path_from_cod(cod)
        data_files = unzip(file_path,out=tempdir)
        fp = Files()
        fp.new(path=tempdir,url='unzipe-file')
        fp.save()
        return fp.cod, [ Path(tempdir)/file for file in data_files ]

    def join(self,all_files: list) -> pd.DataFrame:
        try:
            return pd.concat((pd.read_csv(f, sep=';', encoding='ANSI') for f in all_files), ignore_index=True)
        except LookupError:
            return pd.concat((pd.read_csv(f, sep=';',encoding='ISO-8859-1') for f in all_files), ignore_index=True)

    def make_files(self, df : pd.DataFrame) -> str:
        tempdir = mkdtemp()

        df["INDICADOR_AJUIZADO"] = df["INDICADOR_AJUIZADO"] == 'SIM'
        df['PESSOA_FISICA'] = df['TIPO_PESSOA'] == 'Pessoa física'
        df['DEVEDOR_PRINCIPAL'] = df['TIPO_DEVEDOR']=='PRINCIPAL'

        df.drop('TIPO_PESSOA', inplace=True, axis=1)
        df.drop('TIPO_DEVEDOR', inplace=True, axis=1)
        df.drop('NOME_DEVEDOR', inplace=True, axis=1)
        df.drop('CPF_CNPJ', inplace=True, axis=1)
        df.drop('UNIDADE_RESPONSAVEL', inplace=True, axis=1)
        df.drop('RECEITA_PRINCIPAL', inplace=True, axis=1)

        df[df['PESSOA_FISICA']].to_csv(Path(tempdir)/'pessoa_fisica.csv',encoding='utf8',index_label='line')
        df[~df['PESSOA_FISICA']].to_csv(Path(tempdir) / 'pessoa_juridica.csv', encoding='utf8',index_label='line')
        df[df['DEVEDOR_PRINCIPAL']].to_csv(Path(tempdir) / 'devedor_principal.csv', encoding='utf8',index_label='line')
        df[~df['DEVEDOR_PRINCIPAL']].to_csv(Path(tempdir) / 'devedor_corresponsavel.csv', encoding='utf8',index_label='line')
        df[df['INDICADOR_AJUIZADO']].to_csv(Path(tempdir) / 'acao_ajuizada.csv', encoding='utf8',index_label='line')
        df[~df['INDICADOR_AJUIZADO']].to_csv(Path(tempdir) / 'acao_nao_ajuizada.csv', encoding='utf8',index_label='line')
        return tempdir

    def prepare(self, cod: str) -> str:
        prepared_cod, files = self.unzip(cod)
        tempdir = self.make_files(self.join(files))
        f = Files()
        f.new(path=tempdir,url='prepared-files')
        f.save()
        return f.cod

#TODO: fazer o envio dos arquivos para o S3
#TODO: fazer o clico para o bacen

class Bacen(DataCrawlerInterface):
    pass