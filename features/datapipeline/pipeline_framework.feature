# Created by zahidg at 28-12-21
Feature: Movimiento de un archivo landing a bigquery y gcs
"""
  Se espera que exista un Pipeline que tome un archivo .csv desde una zona landing
  y lo envíe a un bucket raw, posteriormente ejecute una ETL, y los resultados sean guardados
  en bigquery y en storage.
  """

  Scenario: El archivo result.csv llega al bucket landing y se ejecuta la ETL
    Given el workflow metacritic deployado en GCP
    And el template result_csv en un bucket de artefactos
    And el archivo src/test/resources/data/result.csv en un bucket landing
    Then se valida el archivo consolidado en raw con el nombre result.csv
    Then se valida la existencia de la tabla metacritic_model en el dataset staging con los datos del archivo
    Then se valida la existencia de los ["top_10.csv"] en el bucket de analytics


  Scenario: El archivo consoles.csv llega al bucket landing y se ejecuta la ETL
    Given el workflow consoles_dim deployado en GCP
    And el template consoles_csv en un bucket de artefactos
    And el archivo src/test/resources/data/consoles.csv en un bucket landing
    Then se valida el archivo consolidado en raw con el nombre consoles.csv

