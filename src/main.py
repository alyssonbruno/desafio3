from typing import Optional

from flask import Flask
from config_aws import S3Config
from tempfile import mkstemp

from download import download


app = Flask(__name__)
s3 = S3Config()


@app.route("/download/<string:tipo>/", methods=['GET'])
def download_route(tipo : Optional[str] = None):
    from os import environ
    url_pgfn = environ[
        'URL_ARQUIVO_PGFN'] if 'URL_ARQUIVO_PGFN' in environ else 'http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip'
    if tipo == 'pgfn':
        _, temp_file_name = mkstemp(suffix='.zip')
        ret = download(url_pgfn,file_name=temp_file_name)
        return {'msg': ret}, 200
    else:
        return {'msg': 'erro in download'}, 403


@app.route("/")
def index():
    return {'msg': 'ok'}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
