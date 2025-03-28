
-- File Path: Make sure to set the correct file path based on where the CSV file is stored on your machine or server. 
-- The paths provided in the examples are specific to one environment (Windows in this case). 
-- You must update them to reflect the actual location of the file on your system.

-- 1. Execute via Terminal with psql:
-- To import the data from the CSV file into the relatorio_cadop table using the psql command-line tool, 
-- run the following command:

\COPY relatorio_cadop FROM 'C:\\{YOUR_FILE_PATH}\\Teste_de_Banco_de_Dados\\Relatorio_cadop.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'utf-8')


-- 2. Execute via Server Query:
-- To import data directly from the server side, use the following COPY command. 
-- Keep in mind that your PostgreSQL server must have permission to access and read the file.

COPY relatorio_cadop FROM 'C:\\{YOUR_FILE_PATH}\\Teste_de_Banco_de_Dados\\Relatorio_cadop.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'utf-8')