from fastinference.managers.task_manager import TasksManager
from fastinference.data_processing.datablock import DataBlock

from typing import List, Tuple, Dict
from itertools import chain

import pandas as pd
import numpy as np
import os


def extract_response_only(data: List[DataBlock], task_manager: TasksManager) -> List:
    def get_response(data):
        return data.response.choices[0].message.content

    return task_manager.build_multithread(get_response, data, "Building the LLM Response only")


def extract_from_file(path: str,
                      column_main_content: str,
                      task_manager: TasksManager,
                      nb_chunks: int = 20) -> List[Tuple[str, Dict]]:
    def extract_chunks(data_chunk: pd.DataFrame, column_main_content: str) -> List[Tuple[str, Dict]]:
        result = []
        for index, row in data_chunk.iterrows():
            main_content = row[column_main_content]
            other_data = {col: row[col] for col in data_chunk.columns if col != column_main_content}
            result.append((main_content, other_data))
        return result

    # Identify the file extension
    _, file_extension = os.path.splitext(path)
    file_extension = file_extension.lower()

    # Read data based on file extension
    if file_extension == ".csv":
        data = pd.read_csv(path)
    elif file_extension == ".xlsx":
        data = pd.read_excel(path)
    elif file_extension == ".json":
        data = pd.read_json(path)
    elif file_extension == ".parquet":
        data = pd.read_parquet(path)
    else:
        raise ValueError("Unsupported file type")

    # Split data into chunks
    data_chunks = np.array_split(data, nb_chunks)

    # Use the task manager to process data chunks in parallel
    list_formatted = task_manager.build_multithread(extract_chunks,
                                                    data_chunks,
                                                    f"Formating the {file_extension} file",
                                                    column_main_content=column_main_content)

    # Flatten the list of results from all chunks
    list_flatten = list(chain.from_iterable(list_formatted))

    return list_flatten

