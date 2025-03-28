
-- File Path: Ensure the file path is correct based on the location of the CSV file on your machine or server. 
-- The paths in the examples are specific to a Windows environment, so you must
-- update them to match the actual location of the file on your system.
--
-- Read permission SERVER SIDE ONLY: Ensure that the PostgreSQL server has read permissions for the CSV files 
-- when performing a COPY operation with server-side queries.
--
-- Help: To grant read access, simply provide basic read permissions 
-- to all users (i.e., "Everyone" on Windows or "Todos" on Portuguese-Brazil systems) 
-- for the demonstracoes_contabeis and relatorio_cadop folders.



-- IMPORTING relatorio_cadop.csv

-- 1.(Client Side) Execute via Terminal with psql (Import: Make sure you change the path correctly for your device):
-- To import the data from the CSV file into the relatorio_cadop table using the psql command-line tool (CLI), 
-- run the following command:
\COPY relatorio_cadop FROM 'C:\\{YOUR_FILE_PATH}\\Teste_de_Banco_de_Dados\\relatorio_cadop\\Relatorio_cadop.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'utf-8')


-- 2.(Server Side) Execute via Server Query (Import: Make sure you change the path correctly for your device):
-- To import data directly from the server side, use the following COPY command. 
-- Keep in mind that your PostgreSQL server must have permission to access and read the file.
COPY relatorio_cadop FROM 'C:\\{YOUR_FILE_PATH}\\Teste_de_Banco_de_Dados\\relatorio_cadop\\Relatorio_cadop.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'utf-8')



-- IMPORTING demonstracoes_contabeis files for 2023 and 2024

-- 2. (Server Side) Execute via Server Query
-- Import: Make sure you change the path correctly for your device
-- Don't be afraid, it will take a while, there are a total of 6256861 lines adding up all the files
DO $$ 
DECLARE 
    i INT;
	year INT;
    file_path TEXT;
BEGIN
    -- Loop through the range (1T, 2T, 3T, 4T)
    FOR i IN 1..4 LOOP  
        -- Loop over both years (2023 and 2024)
        FOR year IN 2023..2024 LOOP
            -- Build the file path dynamically
            file_path := 'C:\\Users\\vitor.DESKTOP-V9RV4P3\\Downloads\\vitor\\Teste_Intuitive_Care\\Teste_de_Banco_de_Dados\\demonstracoes_contabeis\\' || i || 'T' || year || '.csv';
            
            -- Execute the COPY command with dynamic file path
			-- Important: specify columns to ignore id column when reading the csv
            EXECUTE 'COPY demonstracoes_contabeis (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) FROM ' || quote_literal(file_path) || ' WITH (FORMAT csv, DELIMITER '';'' , HEADER true, ENCODING ''utf-8'')';
              
        END LOOP;
    END LOOP;
END $$;
