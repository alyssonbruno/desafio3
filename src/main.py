from typing import Optional

from flask import Flask
from config_aws import S3Config
from service import PGFN, Bacen


app = Flask(__name__)
s3 = S3Config()
tipos = {
    'pgfn': PGFN(),
    'bacen': Bacen()
}

@app.route("/download/<string:tipo>", methods=['GET'])
@app.route("/download/<string:tipo>/", methods=['GET'])
def download_route(tipo : Optional[str] = None):
    if tipo in ('pgfn', 'bacen'):
        cod = tipos[tipo].download()
        return {'file': {'cod': cod}}, 200
    else:
        return {'msg': 'erro in file tipy for download'}, 404

@app.route("/prepare/<string:tipo>/<uuid:cod_file>", methods=['GET'])
@app.route("/prepare/<string:tipo>/<uuid:cod_file>/", methods=['GET'])
def prepare_route(tipo : Optional[str] = None, cod_file : Optional[str] = None):
    if tipo in ('pgfn', 'bacen'):
        cod = tipos[tipo].prepare(str(cod_file))
        return {'file': {'cod': cod}}, 200
    else:
        return {'msg': 'erro in file tipy for download'}, 404


@app.route("/")
def index():
    return {'msg': 'ok'}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8663')
