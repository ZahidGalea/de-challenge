# Created by zahidg at 28-12-21
Feature: Movimiento de un archivo landing a bigquery y gcs
"""
  Se espera que exista un Pipeline que tome un archivo .csv desde una zona landing
  y lo envíe a un bucket raw, posteriormente ejecute una ETL, y los resultados sean guardados
  en bigquery y en storage.
  """

  Scenario: El archivo result.csv llega al bucket landing y se ejecuta la ETL
    Given el workflow metacritic deployado en GCP
    And el template dataflow_templates/result_csv.json en un bucket de artefactos
    And el archivo tests/resources/data/result.csv en un bucket landing con el nombre result.csv
    Then se valida el archivo consolidado en raw con el nombre result/result.csv
    Then se valida la existencia de los ["top_10_games_.*csv.*","top_10_games_by_console_.*csv-.*","worst_10_games_.*csv-.*","worst_10_games_by_console_.*csv-.*"] en el bucket de analytics
    Then se valida la existencia de la tabla metacritic_model en el dataset staging con los datos del archivo


  Scenario: El archivo consoles.csv llega al bucket landing y se ejecuta la ETL
    Given el workflow consoles_dim deployado en GCP
    And el archivo tests/resources/data/consoles.csv en un bucket landing con el nombre consoles_dim.csv
    Then se valida el archivo consolidado en raw con el nombre consoles/consoles.csv


  Scenario: El archivo sindefinicion.csv llega al bucket landing y se ejecuta la ETL
    Given el workflow undefined_files deployado en GCP
    And el archivo tests/resources/data/sindefinicion.csv en un bucket landing con el nombre sindefinicion.csv
    Then se valida el archivo consolidado en raw con el nombre undefined/sindefinicion.csv

