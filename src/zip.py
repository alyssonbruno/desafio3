#!/bin/env python
# descompacta arquivos
from typing import Optional
from zipfile import ZipFile
from shutil import copyfileobj
from pathlib import Path

DEFAULT_OUTPUT_DIR = '.'

def unzip(file_name: str, out: Optional[str] = None) -> None:
    """descompacta o arquivo passado como parâmetro.
    >>> unzip('Dados_abertos_Nao_Previdenciario.zip')
    ['arquivo_lai_SIDA_AC_202012.csv', 'arquivo_lai_SIDA_AL_202012.csv', 'arquivo_lai_SIDA_AM_202012.csv', 
    'arquivo_lai_SIDA_AP_202012.csv', 'arquivo_lai_SIDA_BA_202012.csv', 'arquivo_lai_SIDA_CE_202012.csv', 
    'arquivo_lai_SIDA_DF_202012.csv', 'arquivo_lai_SIDA_ES_202012.csv', 'arquivo_lai_SIDA_GO_202012.csv', 
    'arquivo_lai_SIDA_MA_202012.csv', 'arquivo_lai_SIDA_MG_202012.csv', 'arquivo_lai_SIDA_MS_202012.csv', 
    'arquivo_lai_SIDA_MT_202012.csv', 'arquivo_lai_SIDA_PA_202012.csv', 'arquivo_lai_SIDA_PB_202012.csv', 
    'arquivo_lai_SIDA_PE_202012.csv', 'arquivo_lai_SIDA_PI_202012.csv', 'arquivo_lai_SIDA_PR_202012.csv', 
    'arquivo_lai_SIDA_RJ_202012.csv', 'arquivo_lai_SIDA_RN_202012.csv', 'arquivo_lai_SIDA_RO_202012.csv', 
    'arquivo_lai_SIDA_RR_202012.csv', 'arquivo_lai_SIDA_RS_202012.csv', 'arquivo_lai_SIDA_SC_202012.csv', 
    'arquivo_lai_SIDA_SE_202012.csv', 'arquivo_lai_SIDA_SP_202012.csv', 'arquivo_lai_SIDA_TO_202012.csv']
    >>> unzip(None)
    Traceback (most recent call last):
    ...
    TypeError: file_name must be informed
    >>>
    """
    output_dir = DEFAULT_OUTPUT_DIR if out is None else out
    files = []
    if file_name is None or file_name == "":
        raise TypeError('file_name must be informed')
    zip_file = ZipFile(file_name)
    for inner_file_name in zip_file.namelist():
        output_file_path = Path(f'{output_dir}/{inner_file_name}')
        with zip_file.open(inner_file_name) as inner_file:
            with open(output_file_path, mode='wb') as output_file:
                copyfileobj(inner_file,output_file)
                files.append(inner_file_name)
    return files

if __name__ == "__main__":
    from sys import argv
    if len(argv)<2:
        print("Usage: zip filename.zip")
        exit(1)
    unzip(argv[1])