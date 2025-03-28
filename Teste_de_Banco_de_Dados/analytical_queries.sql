
-- Expenses from the last trimester of 2024

-- Filter by the specified description and expenses from the last trimester of 2024
-- Order by ASC to get the highest expenses
-- Limit the results to the top 10 entries
SELECT *,  ABS((vl_saldo_final - vl_saldo_inicial)::NUMERIC)::MONEY AS despesa  FROM demonstracoes_contabeis AS dc 
WHERE TRIM(dc.descricao) = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND dc.data >= '2024-10-01'
ORDER BY (vl_saldo_final - vl_saldo_inicial) ASC
LIMIT 10


-- Expenses for the entire year of 2024

-- Filter by the specified description and expenses for 2024
-- Order by ASC to get the highest expenses
-- Limit the results to the top 10 entries
SELECT *,  ABS((vl_saldo_final - vl_saldo_inicial)::NUMERIC)::MONEY AS despesa  FROM demonstracoes_contabeis AS dc 
WHERE TRIM(dc.descricao) = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND dc.data >= '2024-01-01'
ORDER BY (vl_saldo_final - vl_saldo_inicial) ASC
LIMIT 10
