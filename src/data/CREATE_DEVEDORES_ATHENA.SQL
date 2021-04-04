CREATE EXTERNAL TABLE IF NOT EXISTS dcstone.devedores (
  `line` int,
  `UF_UNIDADE_RESPONSAVEL` string,
  `NUMERO_INSCRICACAO` string,
  `TIPO_SITUACAO_INSCRICAO` string,
  `SITUACAO_INSCRICAO` string,
  `DATA_INSCRICAO` date,
  `INDICADOR_AJUIZADO` boolean,
  `VALOR_CONSOLIDADO` double,
  `PESSOA_FISICA` boolean,
  `DEVEDOR_PRINCIPAL` boolean
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://dcstone/'
TBLPROPERTIES ('has_encrypted_data'='false');