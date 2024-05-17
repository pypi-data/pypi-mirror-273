import re
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
import os
import pyperclip
import snowflake.connector as snow
import warnings
load_dotenv(find_dotenv('../.env'))
import openai
import logging

from cdbt.prompts import Prompts
from cdbt.main import ColdBoreCapitalDBT

# Have to load env before import openai package.
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger('snowflake.connector').setLevel(logging.WARNING)


class BuildUnitTestDataAI:

    def __init__(self):
        self.model = 'gpt-4o'
        # Make sure you have OPENAI_API_KEY set in your environment variables.
        self.client = openai.OpenAI()

        self.prompts = Prompts()
        self._conn = None
        self._cur = None
        self._create_snowflake_connection()

    def _create_snowflake_connection(self):
        self._conn = snow.connect(
            account=os.environ.get('DATACOVES__MAIN__ACCOUNT'),
            password=os.environ.get('DATACOVES__MAIN__PASSWORD'),
            schema=os.environ.get('DATACOVES__MAIN__SCHEMA'),
            user=os.environ.get('DATACOVES__MAIN__USER'),
            warehouse=os.environ.get('DATACOVES__MAIN__WAREHOUSE'),
            database=os.environ.get('DATACOVES__MAIN__DATABASE'),
            role=os.environ.get('DATACOVES__MAIN__ROLE'),
        )

        self._cur = self._conn.cursor()

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

        file_path = self._get_file_path(model_name)
        # # Extract the folder immediately after 'models'. Not sure I need to use this just yet, hodling on to it for later.
        layer_name = file_path.split('/')[1][:2]
        sub_folder = file_path.split('/')[2]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        test_file_path = f'tests/unit_tests/{layer_name}/{sub_folder}/test_{file_name}.sql'

        input_sql_file_name = file_path

        input_sql = self.read_file(input_sql_file_name)

        models_in_model_file = self.extract_model_names(input_sql)

        sample_data = self._get_sample_data_from_snowflake(models_in_model_file)

        prompt = self.build_prompt(self.prompts.build_unit_test_prompt, model_name, input_sql, sample_data)

        messages = [
            {"role": "system", "content": "You are helping to build unit tests for DBT (database build tools) models."},
            {"role": "user", "content": prompt}
        ]

        response = self.send_message(messages)

        output = self._remove_first_and_last_line_from_string(response)
        print(output)

        clip_or_file = input(f'1. to copy to clipboard\n2, to write to file ({test_file_path}')

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

    def _get_file_path(self, model_name):
        cdbt_main = ColdBoreCapitalDBT()
        # This will get the path of the model. note, that unit tests show up as models, so must be excluded via the folder.
        #
        args = ['--select', model_name, '--output', 'json', '--output-keys', 'original_file_path', '--exclude',
                'path:tests/* resource_type:test']
        model_ls_json = cdbt_main.dbt_ls_to_json(args)
        file_path = model_ls_json[0]['original_file_path']
        return file_path

    def _remove_first_and_last_line_from_string(self, s: str) -> str:
        return '\n'.join(s.split('\n')[1:-1])

    def _get_sample_data_from_snowflake(self, model_names: List[str]):
        """
        Compiles the target model to SQL, then breaks out each sub query and CTE into a separate SQL strings, executing
        each to get a sample of the data.
        Args:
            model_name: A list of target model names to pull sample data from.

        Returns:

        """
        cdbt_main = ColdBoreCapitalDBT()
        sample_results = {}
        for model_name in model_names:
            args = ['--select', model_name, '--full-refresh']
            cmd = 'compile'
            cdbt_main.execute_dbt_command_stream(cmd, args)
            results = cdbt_main.execute_dbt_command_capture(cmd, args)
            extracted_sql = self.extract_sql(results)
            sample_sql = self.build_sample_sql(extracted_sql)
            self._cur.execute(sample_sql)
            tmp_df = self._cur.fetch_pandas_all()
            sample_results[model_name] = tmp_df.to_csv(index=False)
            a = 0
        return sample_results

    @staticmethod
    def build_sample_sql(sql: str) -> str:
        sql = f'''
        with tgt_table as (
            {sql}
        )
        select * 
        from tgt_table
        sample (20 rows)
        '''
        return sql

    @staticmethod
    def extract_sql(log):
        sql_lines = [line for line in log.splitlines() if not re.match(r'^\x1b\[0m\d{2}:\d{2}:\d{2}', line)]
        # Join the remaining lines and remove escape sequences
        sql = '\n'.join(sql_lines).replace('\x1b[0m', '').strip()
        return sql

    @staticmethod
    def extract_model_names(dbt_script):
        # Regular expression to find all occurrences of {{ ref('model_name') }}
        pattern = r"\{\{\s*ref\('([^']+)'\)\s*\}\}"
        # Find all matches in the script
        model_names = re.findall(pattern, dbt_script)
        return model_names

    @staticmethod
    def build_prompt(prompt_template: str, model_name: str, model_sql, sample_models_and_data: Dict[str, str]):
        sample_str = ''
        for model_name, sample_data in sample_models_and_data.items():
            sample_str += f'''{model_name}: \n{sample_data}\n'''


        output = f'''
The model name we are building the test for is {model_name}. In the example, this says "model_name". Put this value in that same place.'
{prompt_template}

The SQL for the model is:
{model_sql}

Here is sample data for each input model. This just represents a random sample. Use it to create realistic test data, but try to build the test input data so that it tests the logic found within the model, regardless of the particular combination of sample data. Imagine that certain flags might be true or false, even if that flag is always true or false in the sample data. 

{sample_str}

'''
        return output



if __name__ == '__main__':
    BuildUnitTestDataAI().main('appointment_revenue_mrpv_metrics')
