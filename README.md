# Data Challenge Stone - Desafio #3
Este repositório contém minha resposta ao desafio #3 da Data Challenge Stone - Área de Engenharia de Dados.

O nome do bucket utiliado deverá ser configurado no arquivo aws.toml (dentro do diretório src)

## instalação com Docker
Use o arquivo Dockerfile para criar a imagem base para aplicar o teste: `docker build .` então rode o docker com o container passando a chave de sua conta AWS na variável de ambiente AWS_S3_KEY e as URLS alvo nas variáveis de ambiente URL_ARQUIVO_PGFN e URL_ARQUIVO_BACEN. Exemplo:
```shell
docker image build . --tag dcstone
docker run -p 8663:80 --env AWS_SECRET_ACCESS_KEY=/2jQeiT5Q844XEsAXILBKO7R/qh2cvpB/9f0IewG --env AWS_ACCESS_KEY_ID=AKIAWCDAQWITPLYUVL4A --env URL_ARQUIVO_PGFN=http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip --rm dcstone
```

## instalação com Python
É necessário ter o python 3.8+ instalado e com o pip funcionado.
```shell
export AWS_SECRET_ACCESS_KEY=/2jQeiT5Q844XEsAXILBKO7R/qh2cvpB/9f0IewG 
export AWS_ACCESS_KEY_ID=AKIAWCDAQWITPLYUVL4A
export URL_ARQUIVO_PGFN=http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip
python -m pip install -r requeriments.txt
python src/main.py
```

## consumindo o serviço
Todo o desafio foi dividido em 3 etapas para cada tarefa (PGFN e Bacen), a estapas são: baixar os arquivos, processá-los e enviá-los à AWS. Existe um endpoint guarda-chuva que fará todo o processamento para comprimento do desafio, com o serviço rodando faça:
```shell
curl -sL http://localhost:8663/do-it
```
