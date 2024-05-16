import asyncio

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from tqdm import tqdm
from typing import List, Callable

from fastinference.data_processing.datablock import DataBlock


class TasksManager:
    def __init__(self, nb_thread: int = None) -> None:
        self.nb_thread = nb_thread

    def build_multithread(self, function_to_execute: Callable, data: list, task_name: str, **kwargs) -> List:
        tasks = []

        func_with_kwargs = partial(function_to_execute, **kwargs)
        with ThreadPoolExecutor(max_workers=self.nb_thread) as executor:
            future_to_date = {executor.submit(func_with_kwargs, content) for content in data}
            for future in tqdm(as_completed(future_to_date), total=len(future_to_date), desc=task_name):
                result = future.result()
                if result is not None:
                    tasks.append(result)

        return tasks

    async def build_async(self,
                          function_to_execute: Callable,
                          datablock_chain: List[DataBlock],
                          **kwargs) -> List[asyncio.Task]:

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor(max_workers=self.nb_thread) as executor:
            futures = [executor.submit(self.prepare_task, loop, function_to_execute, block, **kwargs)
                       for block in datablock_chain]
            tasks = [future.result() for future in futures]

        return tasks

    def prepare_task(self, loop, function_to_execute, prompt_object, **kwargs):
        return loop.create_task(function_to_execute(prompt_object, **kwargs))

