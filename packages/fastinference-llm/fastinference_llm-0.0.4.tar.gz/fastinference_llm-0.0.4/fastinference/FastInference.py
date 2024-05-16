from fastinference.managers.llm_manager import LLMManager
from fastinference.managers.task_manager import TasksManager
from fastinference.data_processing.data_processor import DataProcessor
from fastinference.utils.data_processing import extract_from_file, extract_response_only

import asyncio


class FastInference:
    def __init__(self, file_path: str, main_column: str, prompt: str, only_response: bool = False, **kwargs):
        self.llm_manager = LLMManager(**kwargs)
        self.task_manager = TasksManager()
        self.file_path = file_path
        self.main_column = main_column
        self.prompt = prompt
        self.only_response = only_response

    def run(self):
        return asyncio.run(self.run_process())

    async def run_process(self):
        # Build the DataBlockChain
        data_loaded = extract_from_file(self.file_path,
                                        self.main_column,
                                        self.task_manager)[:200]

        data = DataProcessor(data_loaded, self.task_manager, prompt=self.prompt)

        # Run the LLM
        tasks = await self.task_manager.build_async(self.llm_manager.get_acompletion, data.datablock_chain)
        results = await asyncio.gather(*tasks)

        if self.only_response:
            return extract_response_only(results, self.task_manager)
        else:
            return results