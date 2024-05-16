# Author: Yoaz Menda
import csv
import logging
import os
from datetime import datetime
from typing import List, Literal, Tuple

from prompeteer.providers.llm_request import ILLMRequest
from prompeteer.providers.llm_client import ILLMClient, get_llm_client
from prompeteer.prompt.prompt import Variable
from prompeteer.prompt.prompt_config import load_prompt_config, PromptConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

clients = {}


def run_prompt(prompt_config_file_path: str,
               input_csv: str,
               output_csv: str = None,
               destination: Literal['file', 'console'] = 'console',
               row_numbers_to_process: List[int] = None,
               include_prompt: bool = False):
    results = _run_prompts(input_csv, prompt_config_file_path, row_numbers_to_process)
    if destination == 'console':
        handle_console(include_prompt, results)
    elif destination == 'file':
        handle_file(results, include_prompt, input_csv, output_csv)


def _run_prompts(input_csv: str, prompt_config_file_path: str, row_numbers_to_process: List[int]) -> List[
    Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    prompt_config: PromptConfig = load_prompt_config(prompt_config_file_path)
    # Open the input CSV file and process each row
    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='|', quotechar='"')
        for csv_row_number, variables_row in enumerate(reader):
            if row_numbers_to_process is None or csv_row_number in row_numbers_to_process:
                try:
                    variables_to_inject: List[Variable] = [Variable(name, value) for name, value in variables_row.items()]
                    llm_request: ILLMRequest = prompt_config.to_llm_request(variables_to_inject)
                    client: ILLMClient = get_llm_client(prompt_config.llm_provider)
                    response: str = client.call(llm_request)
                    results.append((llm_request.get_prompt_text(), response))
                except Exception as e:
                    logger.error(f"Error processing row {csv_row_number}: {e}")
                    continue  # Continue with the next row, logging the error for this one
    return results


def handle_file(results: List[Tuple[str, str]], include_prompt: bool, input_csv: str, output_csv: str = None):
    if output_csv is None:
        # if not provided, create the output csv file in the same location where the input_csv is located
        output_csv = create_output_file_name(os.path.dirname(input_csv), "result")
    with open(output_csv, 'w', newline='') as out_file:
        fieldnames = ['request', 'response'] if include_prompt else ['response']
        writer = csv.DictWriter(out_file, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL,
                                escapechar='\\')
        writer.writeheader()
        for result in results:
            if include_prompt:
                out_row = {
                    'request': result[0].encode('utf_8').decode('unicode_escape'),
                    'response': result[1]
                }
            else:
                out_row = {
                    'response': result[1]
                }
            writer.writerow(out_row)


def handle_console(include_prompt: bool, results: List[Tuple[str, str]]):
    for request, response in results:
        if include_prompt:
            print("Request:", request)
        print("Response:", response)
        print("--------------------------------------------------------------------------------------------")


def create_output_file_name(directory, output_prefix) -> str:
    return os.path.join(directory, f"{output_prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
