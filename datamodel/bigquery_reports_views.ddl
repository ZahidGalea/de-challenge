############
# Report Views
############
# Top 10 games for console, company
CREATE OR REPLACE VIEW
    consumption.top_10_games_console_company AS
SELECT company,
       console,
       name,
       metascore
FROM (
         SELECT company,
                console,
                name,
                metascore,
                ROW_NUMBER() OVER (PARTITION BY company, console ORDER BY metascore DESC) AS ROW_NUMBER
         FROM `consumption.metacritic_model_unnested`)
WHERE ROW_NUMBER <= 10;


# Worst 10 games for console, company
CREATE OR REPLACE VIEW
    consumption.worst_10_games_console_company AS
SELECT company,
       console,
       name,
       metascore
FROM (
         SELECT company,
                console,
                name,
                metascore,
                ROW_NUMBER() OVER (PARTITION BY company, console ORDER BY metascore) AS ROW_NUMBER
         FROM `consumption.metacritic_model_unnested`)
WHERE ROW_NUMBER <= 10;



# - The top 10 best games for all consoles.
CREATE OR REPLACE VIEW consumption.top_10_games AS
SELECT company,
       console,
       name,
       metascore
FROM (
         SELECT company,
                console,
                name,
                metascore,
                ROW_NUMBER() OVER (ORDER BY metascore DESC) AS ROW_NUMBER
         FROM `consumption.metacritic_model_unnested`)
WHERE ROW_NUMBER <= 10;

# - The worst 10 games for all consoles.
CREATE OR REPLACE VIEW consumption.worst_10_games AS
SELECT company,
       console,
       name,
       metascore
FROM (
         SELECT company,
                console,
                name,
                metascore,
                ROW_NUMBER() OVER (ORDER BY metascore) AS ROW_NUMBER
         FROM `consumption.metacritic_model_unnested`)
WHERE ROW_NUMBER <= 10;