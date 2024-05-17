# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Richard_Cui on 2024/5/15 10:45.
import os
import asyncio
import sys

import filetype
import argparse
import logging
from typing import Optional, List

import jsonlines
import openai
from openai import AsyncClient
import pandas as pd
from openai._types import NOT_GIVEN
from tqdm import tqdm


class DataGenerator:
    """To Define and Generate the Data Class for the SFT by LLM."""

    def __init__(self, file_path: str,
                     prompt: str,
                     model: str,
                     batch_size: int = 1,
                     json_output: bool = False,
                     generate_epoch: int = 1,
                     log_level: str = "WARNING",
                     output_file: Optional[str] = None,
                     sheet_names: Optional[List[str]] = None,
                     openai_base_url: Optional[str] = None,
                     openai_api_key: Optional[str] = None,
                     ):
            """
            Initialize the SFTDataGenerator object.

            Args:
                file_path (str): The path to the input file (either a csv or xlsx file).
                prompt (str): The prompt to be used for generating data.
                model (str): The name or ID of the OpenAI model to be used for generation.
                batch_size (int, optional): The batch size for generating data. Defaults to 1.
                json_output (bool, optional): Whether to output the generated data in JSON format. Defaults to False.
                generate_epoch (int, optional): The number of times to generate data. Defaults to 1.
                log_level (str, optional): The log level for the logger. Defaults to "WARNING".
                output_file (str, optional): The path to the output file. If not provided, a default output file will be created.
                sheet_names (List[str], optional): The names of the sheets to be read from an xlsx file. If not provided, all sheets will be read.
                openai_base_url (str, optional): The base URL for the OpenAI API. If not provided, the value from the environment variable OPENAI_API_BASE will be used.
                openai_api_key (str, optional): The API key for the OpenAI API. If not provided, the value from the environment variable OPENAI_API_KEY will be used.
            """
            self.set_logger(log_level)
            try:
                self.data = pd.read_csv(file_path)
            except Exception as e:
                if (sheet_names is None) or ("all" in [x.lower() for x in sheet_names]):
                    xls = pd.ExcelFile(file_path)
                    sheet_names = xls.sheet_names
                    self.logger.warning(f"No special sheet name was set for xlsx file, use all sheets: {sheet_names}.")
                self.data = pd.concat([pd.read_excel(file_path, sheet_name) for sheet_name in sheet_names])

            self.output_file = output_file if output_file is not None else file_path + '.output.jsonl'
            self.client = AsyncClient(
                base_url=openai_base_url if openai_base_url is not None else os.environ.get("OPENAI_API_BASE"),
                api_key=openai_api_key if openai_api_key is not None else os.environ.get("OPENAI_API_KEY")
            )
            self.prompt = prompt
            self.model = model
            self.batch_size = batch_size
            self.json_output = {"type": "json_object"} if json_output else NOT_GIVEN
            self.generate_epoch = generate_epoch

    def set_logger(self, log_level: str):
            """
            Sets up the logger for the class.

            Args:
                log_level (str): The desired log level for the logger.

            Raises:
                ValueError: If an invalid log level is provided.

            Returns:
                None
            """
            self.logger = logging.getLogger(__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            handler_log_level = getattr(logging, log_level, None)

            if not isinstance(handler_log_level, int):
                raise ValueError('Invalid log level: {}'.format(log_level))
            handler.setLevel(handler_log_level)

            self.logger.addHandler(handler)


    # TODO Add the retry decorator for the get_data_sample function.
    async def get_data_sample(self, row_data: dict) -> dict | None:
        """
        Retrieves a data sample by generating a response using the OpenAI GPT model.

        Args:
            row_data (dict): The input data for generating the response.

        Returns:
            dict | None: The updated row_data dictionary with the generated response added,
                            or None if an error occurred during the process.
        """
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": f"Please Generate data follow the given data: {row_data}"}
        ]
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format=self.json_output
            )
            full_response = response.choices[0].message.content
            row_data['gpt-response'] = full_response
            self.logger.info(f"A response was generated by GPT:\n {full_response}")
            return row_data
        except openai.OpenAIError as e:
            self.logger.error(f"An error occurred when trying to get OpenAI response. "
                              f"Please check the RPM/TPM or account balance or other info if you encounter this error: {e}")
            return None

    async def main_loop(self) -> None:
            """
            Executes the main loop for data generation.

            This method iterates over the data and generates samples in batches. The generated data is written to an output file.

            Returns:
                None
            """
            with jsonlines.open(self.output_file, 'a') as f:
                for e in tqdm(range(self.generate_epoch), desc="Main Epoch Loop", position=0):
                    for batch_start in tqdm(range(0, len(self.data), self.batch_size), position=1, desc="Processing Epoch",
                                            leave=False):
                        tasks = [asyncio.create_task(self.get_data_sample(data.to_dict())) for _, data in
                                 self.data[batch_start: batch_start + self.batch_size].iterrows()]
                        result_ = await asyncio.gather(*tasks)
                        result_ = [x for x in result_ if x is not None]
                        for generate_data in result_:
                            f.write(generate_data)
            self.logger.info(f"Data Generation Finished, the output file is saved as {self.output_file}")


def main():
    parser = argparse.ArgumentParser(description="Data Generator for the SFT by LLM.")

    parser.add_argument("--file_path", type=str, required=True, help="file path of the input data.")
    parser.add_argument("--prompt", type=str, required=True, help="prompt for the data generation.")
    parser.add_argument("--model", type=str, required=True, help="OpenAI model for the data generation.")
    parser.add_argument('--log_level', type=str, default='WARNING',
                    help='Set the logging level. Options are DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is WARNING, set INFO for detail response by GPT.')

    parser.add_argument('--sheet_names', metavar='N', type=str, nargs='+', default=None,
                        help="[Optional] the xlsx files sheet's name for handling, default for all sheet. eg. --sheet_names sheet1 sheet2 sheet3")

    parser.add_argument("--output_file", type=str, required=False,
                        help="[Optional] output file path for the data generation.")
    parser.add_argument("--batch_size", type=int, required=False, default=1,
                        help="[Optional] batch size for the data generation, default as 1.")

    parser.add_argument("--generate_epoch", type=int, required=False, default=1,
                        help="generate epoch for the whole table file, default as 1.")

    parser.add_argument("--openai_base_url", required=False, type=str,
                        help="OpenAI API base url, If not given, will use the env "
                             "variable.")

    parser.add_argument("--openai_api_key", required=False, type=str,
                        help="OpenAI API key, If not given, will use the env "
                             "variable.")

    parser.add_argument("--json_output", required=False, action="store_true",
                        help="[Optional] Response format for the chat completion API of OpenAI.")

    if len(sys.argv) == 1:
        sys.argv.append('--help')

    args = parser.parse_args()

    data_generator = DataGenerator(**dict(vars(args)))
    asyncio.run(data_generator.main_loop())


if __name__ == '__main__':
    main()
