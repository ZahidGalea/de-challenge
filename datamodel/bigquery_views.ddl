CREATE OR REPLACE VIEW consumption.metacritic_model AS
SELECT console,
       metascore,
       name,
       SAFE_CAST(userscore AS FLOAT64) as userscore,
       PARSE_DATE("%b %d, %Y", date)   as date,
       company
FROM staging.metacritic_model;


CREATE OR REPLACE VIEW
  consumption.console AS
SELECT
  DISTINCT console,
  company
FROM
  consumption.metacritic_model;


CREATE OR REPLACE VIEW
  consumption.game_score AS
SELECT
  name,
  console,
  date,
  userscore,
  metascore
FROM
  consumption.metacritic_model;
