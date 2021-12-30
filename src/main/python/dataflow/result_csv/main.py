import argparse
import csv
import logging

import apache_beam as beam
from apache_beam import dataframe
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.dataframe.io import read_csv
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from apache_beam.dataframe.convert import to_pcollection


def run(input_file: str,
        analytics_bucket: str,
        staging_dataset: str,
        execution_date: str,
        target_project_id: str,
        raw_bucket: str,
        beam_args):
    options = PipelineOptions(beam_args, save_main_session=True, streaming=False)

    with beam.Pipeline(options=options) as pipeline:
        def add_metadata_to_dataframe(df):
            df["file_origen"] = input_file
            df["execution_Date"] = execution_date
            return df

        # It reads metacritics and consoles files from GCS
        metacritics = pipeline | 'Read from GCS Metacritics' >> read_csv(input_file)
        consoles = pipeline | 'Read from GCS Consoles' >> read_csv(f'gs://{raw_bucket}/consoles/consoles.csv')

        # Sets the index to be able to join in parallelize mode
        metacritics = metacritics.set_index(["console"])
        consoles = consoles.set_index(["console"])
        base = metacritics.merge(consoles, left_index=True, right_index=True, validate="many_to_one")

        with dataframe.allow_non_parallel_operations():
            base = base.reset_index()

        ###################
        # Bigquery Upload
        ###################

        pc_base = to_pcollection(base.astype(str), yield_elements='schemas')
        (pc_base | 'String to BigQuery Row' >> beam.Map(
            lambda string_input: {
                "company": string_input[5],
                "consoles": [
                    {
                        "console_name": string_input[0],
                        "scores": [
                            {
                                "name": string_input[2],
                                "date": string_input[4],
                                "userscore": string_input[3],
                                "metascore": int(string_input[1])
                            }
                        ]
                    }
                ]
            })
         | "Write to BQ" >> WriteToBigQuery(table=f"{target_project_id}:{staging_dataset}.metacritic_model",
                                            schema="SCHEMA_AUTODETECT",
                                            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                                            method="FILE_LOAD"))

        ###################
        # Report Generation
        ###################

        # - The top 10 best games for each console/company. ####
        top_10_games_for_each_console = base[["company", "console", "name", "metascore"]].groupby(
            ["company", "console", "name"]).mean() \
            .nlargest(10, columns=["metascore"], keep='any')

        top_10_games_for_each_console = add_metadata_to_dataframe(top_10_games_for_each_console)
        top_10_games_for_each_console.to_csv(f'gs://{analytics_bucket}/top_10_games_by_console_{execution_date}.csv',
                                             quoting=csv.QUOTE_NONNUMERIC)

        # - The worst 10 games for each console/company. ####
        worst_10_games_for_each_console = base[["company", "console", "name", "metascore"]].groupby(
            ["company", "console", "name"]).mean() \
            .nsmallest(10, columns=["metascore"], keep='any')

        worst_10_games_for_each_console = add_metadata_to_dataframe(worst_10_games_for_each_console)
        worst_10_games_for_each_console.to_csv(
            f'gs://{analytics_bucket}/worst_10_games_by_console_{execution_date}.csv',
            quoting=csv.QUOTE_NONNUMERIC)

        # - The top 10 best games for all consoles. ####
        top_10_games_for_all_consoles = base[["name", "metascore"]].groupby("name").mean() \
            .nlargest(10, columns=["metascore"], keep='any')

        top_10_games_for_all_consoles = add_metadata_to_dataframe(top_10_games_for_all_consoles)
        top_10_games_for_all_consoles.to_csv(f'gs://{analytics_bucket}/top_10_games_{execution_date}.csv',
                                             quoting=csv.QUOTE_NONNUMERIC)

        # - The worst 10 games for all consoles. ####
        worst_10_for_all_consoles = base[["name", "metascore"]].groupby("name").mean(). \
            nsmallest(10, columns=["metascore"], keep='any')

        worst_10_for_all_consoles = add_metadata_to_dataframe(worst_10_for_all_consoles)
        worst_10_for_all_consoles.to_csv(f'gs://{analytics_bucket}/worst_10_games_{execution_date}.csv',
                                         quoting=csv.QUOTE_NONNUMERIC)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        help="Input Cloud Storage file(s) like: result.csv",
    )
    parser.add_argument(
        "--analytics_bucket",
        help="Output bucket where files will be writen",
    )
    parser.add_argument(
        "--staging_dataset",
        help="Dataset where the file will be load into Bigquery",
    )
    parser.add_argument(
        "--execution_date",
        help="Execution date to add to the records and file",
    )
    parser.add_argument(
        "--target_project_id",
        help="Execution date to add to the records and file",
    )
    parser.add_argument(
        "--raw_bucket",
        help="Execution date to add to the records and file",
    )
    args, beam_args = parser.parse_known_args()

    run(
        input_file=args.input_file,
        analytics_bucket=args.analytics_bucket,
        staging_dataset=args.staging_dataset,
        execution_date=args.execution_date,
        target_project_id=args.target_project_id,
        raw_bucket=args.raw_bucket,
        beam_args=beam_args
    )
