# Data Challenge Stone - Desafio #3
Este repositório contém minha resposta ao desafio #3 da Data Challenge Stone - Área de Engenharia de Dados.

## instalação com Docker
Use o arquivo Dockerfile para criar a imagem base para aplicar o teste: `docker build .` então rode o docker com o container passando a chave de sua conta AWS na variável de ambiente AWS_S3_KEY e as URLS alvo nas variáveis de ambiente URL_ARQUIVO_PGFN e URL_ARQUIVO_BACEN. Exemplo:
```shell
docker image build . --tag dcstone
docker run -p 8663:80 --env AWS_S3_KEY=/2jQeiT5Q844XEsAXILBKO7R/qh2cvpB/9f0IewG --env URL_ARQUIVO_PGFN=http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip --rm dcstone
```

## instalação com Python
É necessário ter o python 3.8+ instalado e com o pip funcionado.
```
python -m pip install -r requeriments.txt
python src/main.py
```
