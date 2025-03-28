import logging
import csv
import pathlib
import json
import sys

import itertools
from collections import defaultdict

from datetime import datetime
from docopt import docopt
import argparse
from hipe_evaluation.ner_eval import Evaluator
import os

def find_output_path(path):
    # Normalize and split the path into parts
    path = os.path.normpath(path)
    parts = path.split(os.sep)

    # Replace "prediction" with "eval_results"
    parts = ["eval_results" if part == "prediction" else part for part in parts]

    # Modify the filename
    filename = parts[-1]
    name, ext = os.path.splitext(filename)
    new_filename = name + "-result" + ext
    parts[-1] = new_filename

    # Join everything back into a path
    new_path = os.sep.join(parts)

    # Create the directory if it doesn't exist
    directory = os.path.dirname(new_path)
    os.makedirs(directory, exist_ok=True)

    return new_path

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Compare reference and prediction files.")
    parser.add_argument("f_reference", help="Path to the reference file")
    parser.add_argument("f_prediction", help="Path to the prediction file")
    parser.add_argument("task", help="choose nerc_fine or nerc_coarse")
    args = parser.parse_args()

    COARSE_COLUMNS_HIPE2022 = ["NE-COARSE-LIT"]
    FINE_COLUMNS_HIPE2022 = ["NE-FINE-LIT", "NE-NESTED"]

    if args.task in ("nerc_fine", "nerc_coarse"):
        ner_columns = (
            FINE_COLUMNS_HIPE2022
            if args.task == "nerc_fine"
            else COARSE_COLUMNS_HIPE2022
        )

    evaluator = Evaluator(args.f_reference, args.f_prediction)
    results, results_pertype = evaluator.evaluate(ner_columns, eval_type="nerc")

    out_path = find_output_path(args.f_prediction)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
