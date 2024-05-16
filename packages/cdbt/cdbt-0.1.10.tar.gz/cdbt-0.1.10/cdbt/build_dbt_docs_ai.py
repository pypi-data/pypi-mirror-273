from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
import subprocess
load_dotenv(find_dotenv('../.env'))
# Have to load env before import openai package.
import openai


class BuildDBTDocs:
    """
    # Make sure you have OPENAI_API_KEY set in your environment variables.
    """

    def __init__(self):
        self.client = openai.OpenAI()

    def main(self):
        print('''
        1) Build new DBT documentation.
        2) Check existing DBT documentation against model for missing definitions.
        ''')
        mode = int(input())

        """
        Inputs
        """
        print('Enter any extra information you want to provide to help describe the model. Leave blank if no info is needed: \n')
        extra_info = input()
        sql_file_path = input('Full or relative path to the file to build for: \n')

        if 'l4' in sql_file_path.lower() or 'l3' in sql_file_path.lower():
            system_instructions = self.read_file('automate/tools/system_instructions_gte_l3.txt')
        else:
            system_instructions = self.read_file('automate/tools/system_instructions_lte_l2.txt')

        if mode == 1:
            # Build new documentation

            user_input = self.build_user_msg_mode_1(sql_file_path, extra_info)
        elif mode == 2:
            # Check existing documentation
            yml_file_path = sql_file_path[:-4] + '.yml'
            user_input = self.build_user_msg_mode_2(sql_file_path, yml_file_path, extra_info)
        else:
            print(mode)
            raise ValueError('Invalid mode')

        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_input}
        ]

        assistant_responses = []
        result = self.send_message(messages)
        assistant_responses.append(result)

        messages.append({"role": "assistant", "content": assistant_responses[0]})

        print(assistant_responses[0])

        while True:
            write_or_continue = int(input('Press 1 to write to disk and quit, 2 to make changes: '))
            if write_or_continue == 1:
                if mode == 2:
                    self.backup_existing_yml_file(yml_file_path)
                yml_file_path = sql_file_path.replace('.sql', '.yml')
                output = assistant_responses[0].split('\n')
                output = output[1:-1]
                output = '\n'.join(output)
                with open(yml_file_path, 'w') as file:
                    file.write(output)
                if not self.is_file_committed(yml_file_path):
                    commit_file = input('Press 1 to add to git, any other key to byapss: ')
                    if commit_file == '1':
                        subprocess.run(['git', 'add', yml_file_path])

                break

            next_input = input('Enter your next message - Single line only. (Q to end):')
            if next_input.lower() == 'q' or next_input.lower() == 'quit':
                break
            messages.append({"role": "user", "content": next_input})
            response = self.send_message(messages)
            print(response)
            messages.append({"role": "assistant", "content": response})

        print(messages)

    @staticmethod
    def backup_existing_yml_file(yml_file_path):
        with open(yml_file_path, 'r') as file:
            yml_content = file.read()
        with open(yml_file_path + '.bak', 'w') as file:
            file.write(yml_content)

    def send_message(self, _messages: List[Dict[str, str]]) -> str:
        print('Sending to API')
        completion = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=_messages
        )
        return completion.choices[0].message.content

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, 'r') as file:
            return file.read()

    def build_user_msg_mode_1(self, _sql_file_path: str, extra_info: str) -> str:
        sql = self.read_file(_sql_file_path)
        model_name = _sql_file_path.split('/')[-1].split('.')[0]
        prompt_str = f'Build new DBT documentation for the following SQL query with model name {model_name}'
        if len(extra_info):
            prompt_str += f'\n{extra_info}'
        prompt_str += f'\nSQL File Contents:\n{sql}'
        return prompt_str

    def build_user_msg_mode_2(self, _sql_file_path: str, _yml_file_path: str, extra_info: str) -> str:
        sql = self.read_file(_sql_file_path)
        yml = self.read_file(_yml_file_path)
        model_name = _sql_file_path.split('/')[-1].split('.')[0]
        prompt_str = f'Check for missing columns in the following DBT documentation for the following SQL query with model name {model_name}. Identify any columns in the DBT documentation that do not exist in the SQL and comment them out.'
        if len(extra_info):
            prompt_str += f'\n {extra_info}'
        prompt_str += f'\nYML File Contents:\n{yml}'
        prompt_str += f'\nSQL File Contents:\n{sql}'
        return prompt_str

    @staticmethod
    def is_file_committed(file_path):
        try:
            # Check the Git status of the file
            result = subprocess.run(['git', 'ls-files', '--error-unmatch', file_path],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # If the file is tracked, check if it has any modifications
            status_result = subprocess.run(['git', 'status', '--porcelain', file_path],
                                           stdout=subprocess.PIPE)
            status_output = status_result.stdout.decode().strip()
            # If the output is empty, file is committed and has no modifications
            return len(status_output) == 0
        except subprocess.CalledProcessError:
            # The file is either untracked or does not exist
            return False


if __name__ == '__main__':
    BuildDBTDocs().main()
