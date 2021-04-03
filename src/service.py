from os import environ
from database import Files
from tempfile import mkstemp, mkdtemp

from download import download
from zip import unzip

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

    def unzip(self, cod: str) -> str:
        tempdir = mkdtemp()
        file_path = Files.get_path_from_cod(cod)
        data_files = unzip(file_path,out=tempdir)
        fp = Files()
        fp.new(path=tempdir)
        fp.save()
        return fp.cod


    def prepare(self, cod: str) -> str:
        prepared_cod = self.unzip(cod)
        return prepared_cod


class Bacen(DataCrawlerInterface):
    pass