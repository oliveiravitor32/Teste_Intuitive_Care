CREATE DATABASE ans;

CREATE TABLE demonstracoes_contabeis (
 id BIGSERIAL PRIMARY KEY,
 data DATE NOT NULL,
 reg_ans VARCHAR(15) NOT NULL,
 cd_conta_contabil VARCHAR(20),
 descricao VARCHAR(255),
 vl_saldo_inicial NUMERIC(20,2),
 vl_saldo_final NUMERIC(20,2)
);

CREATE TABLE relatorio_cadop (
 registro_ans VARCHAR(10) PRIMARY KEY,
 cnpj VARCHAR(14) NOT NULL,
 razao_social VARCHAR(200) NOT NULL,
 nome_fantasia VARCHAR(150),
 modalidade VARCHAR(150),
 logradouro VARCHAR(150),
 numero VARCHAR(10),
 complemento VARCHAR(150),
 bairro VARCHAR(150),
 cidade VARCHAR(150),
 uf VARCHAR(2),
 cep VARCHAR(8),
 ddd VARCHAR(2),
 telefone VARCHAR(9),
 fax VARCHAR(8),
 endereco_eletronico VARCHAR(255),
 representante VARCHAR(150),
 cargo_representante VARCHAR(150),
 regiao_de_comercializacao SMALLINT,
 data_registro_ans DATE
);
