############
# Base views
############
CREATE OR REPLACE VIEW consumption.metacritic_model_unnested AS
SELECT company,
       consoles.console_name                  AS console,
       scores.name                            as name,
       PARSE_DATE("%b %d, %Y", scores.date)   AS date,
       scores.metascore                       as metascore,
       SAFE_CAST(scores.userscore AS FLOAT64) AS userscore,
FROM staging.metacritic_model,
     UNNEST(consoles) consoles,
     UNNEST(scores) scores;


CREATE OR REPLACE VIEW
    consumption.console AS
SELECT DISTINCT console,
                company
FROM consumption.metacritic_model_unnested;


CREATE OR REPLACE VIEW
    consumption.game_score AS
SELECT name,
       console,
       date,
       userscore,
       metascore
FROM consumption.metacritic_model_unnested;

