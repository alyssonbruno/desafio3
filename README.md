# Data Challenge Stone - Desafio #3
Este repositório contém minha resposta ao desafio #3 da Data Challenge Stone - Área de Engenharia de Dados.

## instalação
Use o arquivo Dockerfile para criar a imagem base para aplicar o teste: `docker build .` então rode o docker com o container passando a chave de sua conta AWS na variável de ambiente AWS_S3_KEY e as URLS alvo nas variáveis de ambiente URL_ARQUIVO_PGFN e URL_ARQUIVO_BACEN. Exemplo:
```shell
docker container run -d --rm -e AWS_S3_KEY=1223 -e URL_ARQUIVO_PGFN=http://dadosabertos.pgfn.gov.br/Dados_abertos_Nao_Previdenciario.zip datachallengestone:latest