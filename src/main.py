from typing import Optional

from flask import Flask
from config_aws import S3Config
from tempfile import mkstemp

from download import download
from database import Files


app = Flask(__name__)
s3 = S3Config()


@app.route("/download/<string:tipo>/", methods=['GET'])
def download_route(tipo : Optional[str] = None):
    from os import environ
    if tipo == 'pgfn':
        url_pgfn = environ[
            'URL_ARQUIVO_PGFN'] if 'URL_ARQUIVO_PGFN' in environ else 'http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip'
        file_was_downloaded = Files.exists_file(url_pgfn)
        if file_was_downloaded is not None:
            return {'file': {'cod': file_was_downloaded}}, 200
        _, temp_file_name = mkstemp(suffix='.zip')
        ret = download(url_pgfn,file_name=temp_file_name)
        f = Files().new(temp_file_name, url_pgfn)
        f.save()
        return {'file': {'cod': f.cod}}, 200
    else:
        return {'msg': 'erro in download'}, 403


@app.route("/")
def index():
    return {'msg': 'ok'}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8663')
