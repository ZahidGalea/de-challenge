import argparse
import json
import logging
import time
from typing import Any, Dict, List

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# Defines the BigQuery schema for the output table.
METACRITIC_SCHEMA = ",".join(
    [
        "url:STRING",
        "num_reviews:INTEGER",
        "score:FLOAT64",
        "first_date:TIMESTAMP",
        "last_date:TIMESTAMP",
    ]
)


def parse_json_message(message: str) -> Dict[str, Any]:
    """Parse the input json message and add 'score' & 'processing_time' keys."""
    row = json.loads(message)
    return {
        "url": row["url"],
        "score": 1.0 if row["review"] == "positive" else 0.0,
        "processing_time": int(time.time()),
    }


def run(
        input_file: str,
        analytics_bucket: str,
        staging_dataset: str,
        beam_args: List[str] = None) -> None:
    """Build and run the pipeline."""
    options = PipelineOptions(beam_args, save_main_session=True, streaming=False)

    with beam.Pipeline(options=options) as pipeline:
        pass

        # Output the results into BigQuery table.
        # _ = messages | "Write to Big Query" >> beam.io.WriteToBigQuery(
        #     "metacritic", schema=METACRITIC_SCHEMA
        # )


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
    args, beam_args = parser.parse_known_args()

    run(
        input_file=args.input_subscription,
        analytics_bucket=args.output_table,
        staging_dataset=args.window_interval_sec,
        beam_args=beam_args
    )
