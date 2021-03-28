#!/bin/env python
# faz o download do conteúdo de uma url passada como parâmetro
#baseado em https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
from requests import get
from typing import Optional

CHUNK_SIZE=8124

def download(url: str, file_name: Optional[str] = None) -> str:
    """
    Baixa o conteúdo de um site, passado como parâmetro.
    >>> download('http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip', 'saida.zip')
    'saida.zip'
    >>> download('https://www.google.com/', 'google.txt')
    'google.txt'
    >>> 
    """
    local_filename: str = url.split('/')[-1] if file_name is None else file_name
    with get(url, stream=True) as stream:
        stream.raise_for_status()
        with open(local_filename, 'wb') as output_file:
            for chunk in stream.iter_content(chunk_size=CHUNK_SIZE):
                output_file.write(chunk)
    return local_filename

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
        print('Usage: download.py url_to_download')
        exit(1)
    download(argv[1], verbose=True)