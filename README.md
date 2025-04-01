# Teste Intuitive Care

Este projeto consiste em 4 testes, onde cada teste se localiza em uma pasta diferente. Ademais, cada teste possui um objetivo e um conhecimento necessário diferente.

> **Observação**: Para informações sobre o uso de cada programa, consulte o arquivo README localizado na raiz de cada programa.

---

## TESTE DE WEB SCRAPING

Objetivo: Realizar um web scraping buscando por PDFs no site da [ANS](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos).

---

## TESTE DE TRANSFORMAÇÃO DE DADOS

Objetivo: Extrair dados de um PDF, estruturar os dados em um arquivo CSV em formato de tabela e compactar o arquivo em '.zip'.

---

## TESTE DE BANCO DE DADOS

Objetivo: Criar scripts '.sql' que contenham queries para estruturar tabelas dos arquivos CSV dos sites [ANS Demonstrações contábeis](https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/) e [ANS Operadoras de plano de saúde ativas](https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/), 
com o resultado dos últimos dois anos demonstrações contábeis e do relatório de operadoras de plano de saúde ativas. Ademais, ínclui queries para importar estes arquivos em formato CSV e algumas queries analíticas para consulta.

---

## TESTE DE API

Objetivo: Desenvolver uma interface web usando Vue.js que interaja com um servidor em Python, para realizar as buscas no arquivo CSV do relatório de operadoras de plano de saúde ativas do teste de banco de dados, e também uma coleção do Postman para demonstrar o resultado da API.
