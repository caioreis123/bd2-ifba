CREATE TABLE compras (
                       TID INT PRIMARY KEY,
                       leite boolean,
                       cafe boolean,
                       cerveja boolean,
                       pao boolean,
                       manteiga boolean,
                       arroz boolean,
                       feijao boolean
);

-- // import CSV
copy compras FROM '/data.csv' DELIMITER ',' CSV HEADER;