import copy
import pandas as pd
import autopep8
import re
# import code # another way to use REPL
import io
import traceback
import sys
from contextlib import redirect_stdout

from .logger import *


class Code:

    @staticmethod
    def _normalize_indentation(code_segment: str) -> str:
        # Determine the minimum indentation of non-empty lines
        lines = code_segment.strip().split('\n')
        min_indent = min(len(re.match(r'^\s*', line).group()) for line in lines if line.strip())

        # Remove the minimum indentation from each line
        return '\n'.join(line[min_indent:] for line in lines)

    # Method to clean the LLM response, and extract the code.
    @staticmethod
    def extract_code(response: str, provider: str, show_plot=False, model_name: str = "", prompt_strategy: str = "") -> str:
        # Use re.sub to replace all occurrences of the <|im_sep|> with the ```.
        response = re.sub(re.escape("<|im_sep|>"), "```", response)

        # cuts off the response after the first return statement or plt.show() or plt.savefig()
        if "Python-hf" in model_name or (prompt_strategy == "coder_only_completion_functions" and "Magicoder" in model_name):
            pattern = r"(^\s{4,}return\s+.*$|^\s*(plt\.show\(\s*\)|plt\.savefig\(\s*.+\s*\))\s*$)"
            match = re.search(pattern, response, flags=re.MULTILINE)
            print("match:", match)

            if match:
                print("Model returned a match for the pattern - cutting")
                cut_off_point = match.end()
                print("cut_off_point:", cut_off_point)
                response = response[:cut_off_point]
                if "```" in response:
                    response = response + "\n```"
            else:
                print("No match found.")

        # Define a blacklist of Python keywords and functions that are not allowed
        blacklist = ['subprocess', 'sys', 'eval', 'exec', 'socket', 'urllib',
                     'shutil', 'pickle', 'ctypes', 'multiprocessing', 'tempfile', 'glob', 'pty',
                     'commands', 'cgi', 'cgitb',
                     'xml.etree.ElementTree', 'builtins', 'subprocess', 'sys', 'eval', 'exec', 'socket',
                     'urllib', 'shutil', 'pickle',
                     'ctypes', 'multiprocessing', 'tempfile', 'glob', 'pty', 'commands', 'cgi', 'cgitb',
                     'xml.etree.ElementTree', 'builtins', 'os.system', 'os.popen', 'sys.modules',
                     '__import__', 'getattr', 'setattr', 'pickle.loads', 'execfile', 'exec', 'compile',
                     'input', 'ast.literal_eval'
                     ]  # TODO: add 'os'?

        # Use a regular expression to find all code segments enclosed in triple backticks with "python"
        if provider == "local":
            code_segments = re.findall(r'```(?:python\s*)?(.*?)\s*```', response, re.DOTALL)
        else:
            if "```python" not in response:
                response = "```python\n" + response + "\n```"
            code_segments = re.findall(r'```python\s*(.*?)\s*```', response, re.DOTALL)
        # Use a regular expression to find all code segments enclosed in triple backticks with or without "python"
        # print("code_segments:", code_segments)
        # code_segments = re.findall(r'```(?:python\s*)?(.*?)\s*```', response, re.DOTALL)
        if not code_segments:
            code_segments = re.findall(r'\[PYTHON\](.*?)\[/PYTHON\]', response, re.DOTALL)

        # Normalize the indentation for each code segment
        normalized_code_segments = [Code._normalize_indentation(segment) for segment in code_segments]

        # Combine the normalized code segments into a single string
        code_res = '\n'.join(normalized_code_segments).lstrip()

        # Remove any instances of "df = pd.read_csv('filename.csv')" from the code
        code_res = re.sub(r"df\s*=\s*pd\.read_csv\((.*?)\)", "", code_res)

        # This is necessary for local OS models, as they are not as good as OpenAI models deriving the instruction from the promt
        if provider == "local":
            # Replace all occurrences of "data" with "df" if "data=pd." is present
            if re.search(r"data=pd\.", code_res):
                code_res = re.sub(r"\bdata\b", "df", code_res)
            # Comment out the df instantiation if it is present in the generated code
            code_res = re.sub(r"(?<![a-zA-Z0-9_-])df\s*=\s*pd\.DataFrame\((.*?)\)",
                              "# The dataframe df has already been defined", code_res)

        if not show_plot:
            if re.search(r"(?<!`)plt\.show\(\)(?!`)", code_res):  # searches for plt.show() not enclosed in backticks
                print(f"{RED}PLT.SHOW() in the code!!!{RESET}:")
                code_res = code_res.replace("plt.show()", "")

        # Define the regular expression pattern to match the blacklist items
        pattern = r"^(.*\b(" + "|".join(blacklist) + r")\b.*)$"

        # Replace the blacklist items with comments
        code_res = re.sub(pattern, r"# not allowed \1", code_res, flags=re.MULTILINE)

        # Return the cleaned and extracted code
        return code_res.strip()

    @staticmethod
    def filter_exec_traceback(full_traceback, exception_type, exception_value):
        # Split the full traceback into lines and filter those that originate from "<string>"
        filtered_tb_lines = [line for line in full_traceback.split('\n') if '<string>' in line]

        # Combine the filtered lines and append the exception type and message
        filtered_traceback = '\n'.join(filtered_tb_lines)
        if filtered_traceback:  # Add a newline only if there's a traceback to show
            filtered_traceback += '\n'
        filtered_traceback += f"{exception_type}: {exception_value}"

        return filtered_traceback

    @staticmethod
    def execute_generated_code(code_str: str, df: pd.DataFrame, tagged_query_type):
        df_copy = copy.deepcopy(df)
        try:
            print(f"{BLUE}EXECUTING THE CODE{RESET}:")
            for i in [1, 2]:
                with redirect_stdout(io.StringIO()) as output:
                    exec(code_str, {'df': df_copy})
                results = copy.deepcopy(output.getvalue())
                if results != "" or tagged_query_type == "plot":
                    break
                print(f"{RED}{i}. Empty exec() output for the 'general' query type!{RESET}")  # caused by no ```python  ``` in llm response or similar
                if i == 2:
                    return "", "empty exec()"
            output.truncate(0)
            output.seek(0)
            print(f"{YELLOW}   FINISHED EXECUTING, RESULTS{MAGENTA}:\n     {results}{RESET}\n")
            return results, None
        except Exception:
            exc_type, exc_value, tb = sys.exc_info()
            full_traceback = traceback.format_exc()
            # Filter the traceback
            exec_traceback = Code.filter_exec_traceback(full_traceback, exc_type.__name__, str(exc_value))
            print(f"{RED}   CODE PRODUCED AN ERROR{RESET}:\n{MAGENTA}     {exec_traceback}{RESET}\n")
            return "ERROR", exec_traceback

    @staticmethod
    def _prepend_imports(code_str: str) -> str:
        return f"import pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n{code_str}"

    @staticmethod
    def _append_result_storage(code_str: str) -> str:
        return code_str + "\n\n" + "result = solve(df)\nprint(result)"

    @staticmethod
    def remove_result_storage_lines(code_str: str) -> str:
        return re.sub(r"result = solve\(df\)\nprint\(result\)", "", code_str)

    @staticmethod
    def _format_to_pep8(code_str: str) -> str:
        # Removes redundant whitespaces and formats the code to PEP8
        return autopep8.fix_code(code_str)

    @staticmethod
    def preprocess_extracted_code(extracted_code: str, prompt_strategy: str) -> str:
        if "import pandas as pd" not in extracted_code or "import matplotlib.pyplot as plt" not in extracted_code:
            extracted_code = Code._prepend_imports(extracted_code)

        if prompt_strategy.endswith("functions"):
            extracted_code = Code._append_result_storage(extracted_code)

        return Code._format_to_pep8(extracted_code)
