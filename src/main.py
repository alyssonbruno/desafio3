from typing import Optional, Dict

from flask import Flask
from config_aws import S3Config
from service import DataCrawlerInterface, PGFN, Bacen


app = Flask(__name__)
s3 = S3Config()
tipos : Dict[str, DataCrawlerInterface] = {
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

@app.route("/send/<string:tipo>/<uuid:cod_file>", methods=['GET'])
@app.route("/send/<string:tipo>/<uuid:cod_file>/", methods=['GET'])
def send_route(tipo : Optional[str] = None, cod_prep : Optional[str] = None):
    if tipo in ('pgfn', 'bacen'):
        cod = tipos[tipo].send(str(cod_prep))
        return {'file': {'cod': cod}}, 200
    else:
        return {'msg': 'erro in file tipy for download'}, 404

@app.route("/do-it", methods=['GET'])
@app.route("/do-it/", methods=['GET'])
def do_it_route():
    ret_cods = []
    for tipo in tipos.keys():
        cod_file = tipos[tipo].download()
        cod_prep = tipos[tipo].prepare(str(cod_file))
        cod_send = tipos[tipo].send(str(cod_prep))
        ret_cods.append({ tipo: {
            'donwload':  {'cod': cod_file},
            'prepare':  {'cod': cod_prep},
            'send':  {'cod': cod_send}
        }})
    return {i[0]:i[1] for i in [k.popitem() for k in ret_cods]}, 200

@app.route("/info/<uuid:cod>", methods=['GET'])
@app.route("/info/<uuid:cod>/", methods=['GET'])
def info_route(cod: str):
    return DataCrawlerInterface.info(str(cod)), 200

@app.route("/")
def index():
    return {'msg': 'ok'}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8663')
