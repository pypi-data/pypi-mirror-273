from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
import os
import pyperclip

load_dotenv(find_dotenv('../.env'))
import openai

from cdbt.prompts import Prompts
from cdbt.main import ColdBoreCapitalDBT

# Have to load env before import openai package.

class BuildUnitTestDataAI:

    def __init__(self):
        self.model = 'gpt-4o'
        # Make sure you have OPENAI_API_KEY set in your environment variables.
        self.client = openai.OpenAI()

        self.prompts = Prompts()

    def send_message(self, _messages: List[Dict[str, str]]) -> object:
        print('Sending to API')
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=_messages
        )
        return completion.choices[0].message.content

    def read_file(self, path: str) -> str:
        with open(path, 'r') as file:
            return file.read()

    def main(self, model_name: str):
        cdbt_main = ColdBoreCapitalDBT()
        # This will get the path of the model. note, that unit tests show up as models, so must be excluded via the folder.
        #
        args = ['--select', model_name, '--output', 'json', '--output-keys', 'original_file_path', '--exclude', 'path:tests/* resource_type:test']
        model_ls_json = cdbt_main.dbt_ls_to_json(args)
        file_path = model_ls_json[0]['original_file_path']
        # # Extract the folder immediately after 'models'. Not sure I need to use this just yet, hodling on to it for later.
        layer_name = file_path.split('/')[1][:2]
        sub_folder = file_path.split('/')[2]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        test_file_path = f'tests/unit_tests/{layer_name}/{sub_folder}/test_{file_name}.sql'

        input_sql_file_name = file_path

        input_sql = self.read_file(input_sql_file_name)

        messages = [
            {"role": "system", "content": self.prompts.build_unit_test_prompt},
            {"role": "user",
             "content": f'The model name is {model_name}. In the example, this says "model_name". Put this value in that same place. SQL: \n {input_sql}'}
        ]

        response = self.send_message(messages)

        output = self._remove_first_and_last_line_from_string(response)
        print(output)

        clip_or_file = input(f'1. to copy to clipboard, 2, to write to file ({test_file_path}')

        if clip_or_file == '1':
            print('Output copied to clipboard')
            pyperclip.copy(output)
        elif clip_or_file == '2':
            # Check if file exists and ask if it should be overwritten.
            if os.path.exists(test_file_path):
                overwrite = input(f'File {test_file_path} exists. Overwrite? (y/n)')
                if overwrite.lower() == 'y':
                    with open(test_file_path, 'w') as file:
                        file.write(output)
                    print(f'Output written to {test_file_path}')
            else:
                with open(test_file_path, 'w') as file:
                    file.write(output)
                print(f'Output written to {test_file_path}')

    def _remove_first_and_last_line_from_string(self, s: str) -> str:
        return '\n'.join(s.split('\n')[1:-1])


if __name__ == '__main__':
    BuildUnitTestDataAI().main('fct_credit_memos_mat')
