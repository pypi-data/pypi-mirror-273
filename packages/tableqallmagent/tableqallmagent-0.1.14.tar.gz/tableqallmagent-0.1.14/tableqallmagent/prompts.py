import json

from .logger import *

class StringOperations:

    @staticmethod
    def prepend_column_desc_and_df_head(column_description, df_head, column_annotations=""):
        tab = " " * 4
        return tab + column_description.replace('\n', '\n' + tab), tab + df_head.replace('\n', '\n' + tab), column_annotations.replace('\n', '\n' + tab)


class PromptsSimple:
    generate_steps_for_plot_save = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, such as names of DataFrame columns.
Make sure to state saving the plot to '{plotname}' in the last step. Do not include showing the plot to the user interactively; only save it to the '{plotname}'.

This algorithm will later be used to write Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm in up to six simple, clear English steps. 
Remember to explain steps rather than to write code.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
2. Extract the 5 rows from the sorted DataFrame.
3. Multiply each found value in the extracted DataFrame by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Save the bar plot to 'plots/example_plot00.png'.
"""

    generate_steps_for_plot_show = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, such as names of DataFrame columns. Make sure to state showing the plot in the last step.

This algorithm will later be used to write Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm in up to six simple, clear English steps. 
Remember to explain steps rather than to write code.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
2. Extract the 5 rows from the sorted DataFrame.
3. Multiply each found value in the extracted DataFrame by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Show the plot.
"""

    generate_steps_no_plot = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, such as names of DataFrame columns.

This algorithm will later be used to write Python code and applied to the existing pandas DataFrame 'df'. 
The DataFrame 'df' is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm with at most six simple, clear English steps. 
Remember to explain steps rather than to write code.
Don't include any visualization steps like plots or charts.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Find and store the minimal value in the 'Speed' column.
2. Find and store the maximal value in the 'Voltage' column.
3. Subtract the minimal speed from the maximal voltage.
4. Raise the result to the third power.
5. Print the result.
"""

    generate_code = """The user provided a query that you need to help achieve: '{input}'. 
You also have a list of subtasks to be accomplished using Python.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return only the Python code that accomplishes the following tasks:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format with backticks:
```python

```
"""

    generate_code_for_plot_save = """The user provided a query that you need to help achieve: '{input}'. 
You also have a list of subtasks to be accomplished using Python.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return only the Python code that accomplishes the following tasks:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must not include `plt.show()`. Just save the plot the way it is stated in the tasks.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format with backticks:
```python

```
"""

    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description, column_annotation):
        return self.generate_steps_no_plot.format(df_head=df_head, input=user_query,
                                                  column_description=column_description,
                                                  column_annotation=column_annotation)

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description, column_annotation):
        return self.generate_steps_for_plot_save.format(input=user_query, plotname=save_plot_name,
                                                        df_head=df_head,
                                                        column_description=column_description,
                                                        column_annotation=column_annotation)

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description, column_annotation):
        return self.generate_steps_for_plot_show.format(input=user_query, df_head=df_head,
                                                        column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        # Plan has already included the plt.show() step, so no need to add it here
        return self.format_generate_code_prompt(df_head=df_head, user_query=user_query, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)


############### Prompts for unit testing coder LLM given a plan ###############:
class PromptsForFunctionGeneration:
    generate_steps_no_plot = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including values necessary to answer the question, such as values to search for, and, most importantly, names of DataFrame columns.

This algorithm will later be used to write a Python function that takes an existing pandas DataFrame 'df' as an argument and returns the result of the analysis. 
The DataFrame 'df' is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm in no more than six simple, clear English steps. 
Focus on explaining the steps rather than writing code. 
Do not include any visualization steps, such as plots or charts. 
You must only output these steps; the code generation assistant will follow them to implement the solution. 
Finally, you must specify the precise value that the function should return.
Preferably, also state the Python data type of the result (e.g. float, DataFrame, list, string, dict, etc.).

Here are examples for your inspiration:

User question: 'What is the maximal voltage minus the minimal speed, but raised to the power of 3?'
Your output:
1. Find and store the minimal value in the 'Speed' column.
2. Find and store the maximal value in the 'Voltage' column.
3. Subtract the minimal speed from the maximal voltage.
4. Raise the result to the power of 3.
5. Return the resulting number.

User question: 'Find four car ids with the largest mileage'
Your output:
1. Sort the DataFrame `df` in descending order based on the 'Mileage' column.
2. Extract the first 4 rows from the sorted DataFrame.
3. Make a list of the 'car_id' column from the extracted DataFrame.
4. Return the list of car ids.
"""

    generate_steps_for_plot_save = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including values necessary to answer the question, such as values to search for and, most importantly, names of DataFrame columns.
Make sure to state saving the plot to '{plotname}' in the last step. Do not include showing the plot to the user interactively; only save it to the '{plotname}'.

This algorithm will later be used to write Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm in no more than six simple, clear English steps. 
Focus on explaining the steps rather than writing code. 
You must only output these steps; the code generation assistant will follow them to implement the solution.

Here's an example for you:

User question: 'Create a bar plot of worst acceleration cars with voltage on the x axis and speed multiplied by 3 on the y axis'
Your output:
1. Sort the DataFrame `df` in descending order based on the 'Acceleration' column.
2. Extract the first 5 rows from the sorted DataFrame.
3. Multiply each 'Speed' value in the extracted DataFrame by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Save the bar plot to 'plots/example_plot00.png'.
"""

    generate_steps_for_plot_show = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including values necessary to answer the question, such as values to search for and, most importantly, names of DataFrame columns.
Make sure to state showing the plot in the last step.

This algorithm will later be used to write Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it.
{df_head}
{column_description}
{column_annotation}
Present your algorithm in up to six simple, clear English steps. 
Remember to explain steps rather than to write code.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example for your inspiration:
User question: 'Create a bar plot of worst acceleration cars with voltage on the x axis and speed multiplied by 3 on the y axis'
Your output:
1. Sort the DataFrame `df` in descending order based on the 'Acceleration' column.
2. Extract the first 5 rows from the sorted DataFrame.
3. Multiply each 'Speed' value in the extracted DataFrame by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Show the plot.
"""

    generate_code = """You are really good with Python and the pandas library. The user provided a query that you need to help achieve: '{input}'. 
You also have a list of subtasks to be accomplished.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return the definition of a Python function called `def solve(df):` that accomplishes the following tasks and returns the result of the analysis if needed:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must use the backticks to enclose the code.
Do not test the function with anything similar to `print(solve(df))`, only define the function, like in the following examples:

Here are examples of the output format:

Example 1:
```python
def solve(df):
    # 1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
    <CODE>
    
    # 2. Extract the 5 rows from the sorted DataFrame.
    <CODE>
    
    # 3. Create a list of the 'Country' column from the extracted DataFrame.
    <CODE>
    
    # 4. Return the list of countries.
    return <RESULT>
```

Example 2:
```python
def solve(df):
    # 1. Find and store the minimal value in the 'Speed' column.
    <CODE>
    
    # 2. Find and store the maximal value in the 'Voltage' column.
    <CODE>
    
    # 3. Subtract the minimal speed from the maximal voltage.
    <CODE>
    
    # 4. Raise the result to the random power.
    <CODE>
    
    # 5. Return the resulting number.
    return <RESULT>
```
"""

    generate_code_for_plot_save = """You are really good with Python and the pandas library. The user provided a query that you need to help achieve: '{input}'. 
You also have a list of subtasks to be accomplished.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return the definition of a Python function called `def solve(df):` that accomplishes the following tasks:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must not include `plt.show()`. Just save the plot the way it is stated in the tasks.
You must use the backticks to enclose the code.
Do not test the function with anything similar to `print(solve(df))`, only define the function, like in the following examples:

Here is an example of the output format:
```python
def solve(df):
    # 1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
    <CODE>
    
    # 2. Extract the 5 rows from the sorted DataFrame.
    <CODE>
    
    # 3. Create a pie plot of the 'GDP' column of the extracted DataFrame.
    <CODE>
    
    # 4. Save the pie plot to 'plots/example_plot00.png'.
    <CODE>
```
"""

    # Here, same as in SimplePrompts, but later could, for example, add column description prompts and methods would be different maybe
    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description, column_annotation):
        return self.generate_steps_no_plot.format(df_head=df_head, input=user_query,
                                                  column_description=column_description,
                                                  column_annotation=column_annotation)

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description, column_annotation):
        return self.generate_steps_for_plot_save.format(input=user_query, plotname=save_plot_name,
                                                        df_head=df_head,
                                                        column_description=column_description,
                                                        column_annotation=column_annotation)

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description, column_annotation):
        return self.generate_steps_for_plot_show.format(input=user_query, df_head=df_head,
                                                        column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        # Plan has already included the plt.show() step, so no need to add it here
        return self.format_generate_code_prompt(df_head, user_query, plan, column_description, column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)


class PromptsSimpleCoderOnly:
    generate_code = """The user provided a query that you need to help achieve: '{input}'.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return only the Python code that accomplishes the user query.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.
Only show the visualizations if the user query explicitly asks for them (plot, chart, etc.).

Example of the output format with backticks:
```python

```
"""

    generate_coder_for_plot_show = """The user provided a query that you need to help achieve: '{input}'.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return only the Python code that accomplishes the user query.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
At the end of the code, show the created visualization with `plt.show()`.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format with backticks:
```python

```
"""

    generate_code_for_plot_save = """The user provided a query that you need to help achieve: '{input}'.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return only the Python code that accomplishes the user query.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must not include `plt.show()`. Just save the plot to '{save_plot_name}' with `plt.savefig('{save_plot_name}')`.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format with backticks:
```python

```
"""

    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "The plan parameter must not be provided for this prompt strategy."
        return self.generate_coder_for_plot_show.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        assert save_plot_name, "The save_plot_name parameter must be provided for this prompt strategy."
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan,
                                                       column_description=column_description,
                                                       save_plot_name=save_plot_name, column_annotation=column_annotation)


class PromptsCoderOnlyForFunctionGeneration:
    generate_code = """You are really good with Python and the pandas library. The user provided a query that you need to help achieve: '{input}'.

A pandas DataFrame named `df` is fixed.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return the definition of a Python function called `def solve(df):` that accomplishes the user query and returns the result of the analysis (a DataFrame, a list, a number, a string, etc.).
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must use the backticks to enclose the code.
Do not test the function with anything similar to `print(solve(df))`, only define the function to answer the user query, in the format of the following example:

Example format:
```python
def solve(df):
    # Code to achieve the user query
    
    # Finally return the result
    return result
```
"""

    generate_code_for_plot_show = """You are really good with Python and the pandas library. The user provided a query that you need to help achieve: '{input}'.

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return the definition of a Python function called `def solve(df):` that accomplishes the user query and returns the result of the analysis.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must use the backticks to enclose the code.
Show the created visualization with `plt.show()`.
Do not test the function with anything similar to `print(solve(df))`, only define the function, in the format of the following example:

Here are examples of the output format:

Example format:
```python
def solve(df):
    # Code to achieve the user query
    
    # Finally show the plot
    plt.show()
```
"""

    generate_code_for_plot_save = """You are really good with Python and the pandas library. The user provided a query that you need to help achieve: '{input}'. 

You have been presented with a pandas DataFrame named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
{df_head}
{column_description}
{column_annotation}
Return the definition of a Python function called `def solve(df):` that accomplishes the user query and returns the result of the analysis.
Basic ibraries are already imported: pandas as pd, matplotlib.pyplot as plt, and numpy as np, so you don't need to import those.
You must not include `plt.show()`. Just save the plot to '{save_plot_name}' with `plt.savefig('{save_plot_name}')`.
You must use the backticks to enclose the code.
Do not test the function with anything similar to `print(solve(df))`, only define the function, in the format of the following example.

Here is an example of the output format:
```python
def solve(df):
    # Code to achieve the user query
    
    # Finally save the plot
    plt.savefig('{save_plot_name}')
```
"""

    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "This prompt strategy does not support generating code from a plan."
        return self.generate_code_for_plot_show.format(input=user_query,
                                                       df_head=df_head,
                                                       column_description=column_description,
                                                       plan=plan,
                                                       column_annotation=column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        assert save_plot_name, "The save_plot_name parameter must be provided for this prompt strategy."
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan,
                                                       column_description=column_description,
                                                       save_plot_name=save_plot_name, column_annotation=column_annotation)


class PromptsCoderOnlyInfillingForFunctionGeneration:
    generate_code = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Args:
        df: pandas DataFrame

    Returns:
        Value that answers the user query (e.g. float, DataFrame, list, string, dict, etc.).
    """
    <FILL_ME>
    return result
```
'''

    generate_code_for_plot_show = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to create and show the plot to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Args:
        df: pandas DataFrame

    Returns:
        None
    """
    <FILL_ME>
    plt.show()
```
'''

    generate_code_for_plot_save = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to create and save the plot to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Function doesn't use `plt.show()`, the plot is only saved to '{save_plot_name}' with `plt.savefig('{save_plot_name}')`.

    Args:
        df: pandas DataFrame

    Returns:
        None
    """
    <FILL_ME>
    plt.savefig('{save_plot_name}')
```
'''

    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "This prompt strategy does not support generating code from a plan."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code_for_plot_show.format(input=user_query, df_head=df_head,
                                                       column_description=column_description,
                                                       plan=plan, column_annotation=column_annotation)

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "This prompt strategy does not support generating code from a plan."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        assert save_plot_name, "The save_plot_name parameter must be provided for this prompt strategy."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan,
                                                       column_description=column_description,
                                                       save_plot_name=save_plot_name, column_annotation=column_annotation)


class PromptsCoderOnlyCompletionForFunctionGeneration:
    generate_code = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Args:
        df: pandas DataFrame

    Returns:
        Variable containing the answer to the task '{input}' (typed e.g. float, DataFrame, list, string, dict, etc.).
    """
    '''

    generate_code_for_plot_show = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to create and show the plot to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Args:
        df: pandas DataFrame

    Returns:
        None, plt.show() is used to display the plot.
    """
    '''

    generate_code_for_plot_save = '''```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def solve(df: pd.DataFrame):
    """ Function to create and save the plot to solve the user query: '{input}'.

    DataFrame `df` is fixed.
    {df_head}
    {column_description}
    {column_annotation}

    Function doesn't use `plt.show()`, the plot is only saved to '{save_plot_name}' with `plt.savefig('{save_plot_name}')`.

    Args:
        df: pandas DataFrame

    Returns:
        None, plt.savefig('{save_plot_name}')
    """
    '''

    def format_generate_steps_no_plot_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_save_prompt(self, df_head, user_query, save_plot_name,
                                                   column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_steps_for_plot_show_prompt(self, df_head, user_query, column_description):
        raise Exception("This prompt strategy does not support generating steps.")

    def format_generate_code_for_plot_show_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "This prompt strategy does not support generating code from a plan."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code_for_plot_show.format(input=user_query,
                                                       df_head=df_head,
                                                       column_description=column_description,
                                                       plan=plan,
                                                       column_annotation=column_annotation)

    def format_generate_code_prompt(self, df_head, user_query, plan, column_description, column_annotation):
        assert not plan, "This prompt strategy does not support generating code from a plan."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description, column_annotation=column_annotation)

    def format_generate_code_for_plot_save_prompt(self, df_head, user_query, plan, column_description,
                                                  save_plot_name="", column_annotation=""):
        assert save_plot_name, "The save_plot_name parameter must be provided for this prompt strategy."
        column_description, df_head, column_annotation = StringOperations.prepend_column_desc_and_df_head(column_description, df_head, column_annotation)
        return self.generate_code_for_plot_save.format(input=user_query, df_head=df_head, plan=plan, column_description=column_description,
                                                       save_plot_name=save_plot_name, column_annotation=column_annotation)


class DebugPrompts:
    basic_debug_prompt = """You are a helpful assistant that corrects the Python code that resulted in an error and returns the corrected code.

The code was designed to achieve this user request: '{input}'.
The DataFrame df that we are working with has already been defined and populated with the necessary data, so there is no need to load or create a new one.
{df_head}
{column_description}
{col_annotation}

The execution of the following code that was by a low-quality assistant resulted in an error:
```python
{code}
```

The error message was: "{error}".

Return only corrected Python code that fixes the error.
Use the same format with backticks.
If part of the code is not defined, or the whole code is a complete nonsense, define or rewrite it.
"""

    completion_debug_prompt = '''The code was designed to achieve this user request: '{input}'.
Here is the code that needs to be fixed:
## Faulty code:
```python
{code}
```

## Error message:
The error message is: "{error}"

Don't test the code by creating new DataFrames or print statements, only correct the code.

## Corrected solution:
{initial_coder_prompt}
'''



class Prompts:
    def __init__(self,
                 str_strategy: str, # one of "simple", "coder_only_simple", "functions", "coder_only_functions", "coder_only_infilling_functions", "coder_only_completion_functions"
                 head_number: int, # number of rows to show in the head of the DataFrame
                 add_column_description: bool = False, # adds json with column names and sample values to the prompt if True
                 n_column_samples: int = 0, # number of sample values to show for each column
                 debug_strategy: str = "basic", # one of "basic", "completion"
                 ):

        self.head_number = head_number
        self.add_column_description = add_column_description
        self.n_column_samples = n_column_samples

        strats = {"simple" : PromptsSimple(),
                  "coder_only_simple" : PromptsSimpleCoderOnly(),
                  "functions": PromptsForFunctionGeneration(),
                  "coder_only_functions": PromptsCoderOnlyForFunctionGeneration(),
                  "coder_only_infilling_functions": PromptsCoderOnlyInfillingForFunctionGeneration(),
                  "coder_only_completion_functions": PromptsCoderOnlyCompletionForFunctionGeneration()}

        debug_strats = {"basic": DebugPrompts.basic_debug_prompt, # str
                        "completion": DebugPrompts.completion_debug_prompt}

        if str_strategy in strats:
            self.strategy = strats[str_strategy]
        else:
            raise Exception(f"{RED}Unknown {CYAN}coder{RED} prompt strategy! See __init__ of Prompts() in prompts.py{RESET}")

        if debug_strategy in debug_strats:
            self.debug_strategy = debug_strats[debug_strategy]
        else:
            raise Exception(f"{RED}Unknown {CYAN}debug{RED} prompt strategy! See __init__ of Prompts() in prompts.py{RESET}")

    def column_description(self, df):  # Changes if we change the 'df' from outside. Creates description dynamically.
        if self.add_column_description:
            start = """\nHere is also a list of column names{sample_values}for your convenience (each column is represented as a separate json object within a list):\n"""
            if self.n_column_samples > 0:
                start = start.format(sample_values=" along with the first sample values ")
                return start + str([{"column_name": c, "sample_values": df[c].head(self.n_column_samples).tolist()} for c in df.columns])
            else: # no sample values included
                return  start.format(sample_values=" ") + str([{"column_name": c} for c in df.columns])
        return ""

    def head_print(self, df):
        if self.head_number > 0:
            return f""" 
The resut of `print(df.head({self.head_number}))` is:
""" + df.head(self.head_number).to_string()
        return ""

    @staticmethod
    def prepend_col_annotation(column_annotation):
        if column_annotation:
            return f"Here is also a JSON description of columns of the DataFrame 'df':\n{json.dumps(column_annotation, indent=4)}"
        return ""

    def generate_steps_no_plot_prompt(self, df, user_query, column_annotation):
        return self.strategy.format_generate_steps_no_plot_prompt(self.head_print(df), user_query,
                                                                  self.column_description(df), self.prepend_col_annotation(column_annotation))

    def generate_steps_for_plot_save_prompt(self, df, user_query, save_plot_name, column_annotation):
        return self.strategy.format_generate_steps_for_plot_save_prompt(self.head_print(df), user_query,
                                                                        save_plot_name, self.column_description(df), self.prepend_col_annotation(column_annotation))

    def generate_steps_for_plot_show_prompt(self, df, user_query, column_annotation):
        return self.strategy.format_generate_steps_for_plot_show_prompt(self.head_print(df), user_query,
                                                                        self.column_description(df), self.prepend_col_annotation(column_annotation))

    def generate_code_prompt(self, df, user_query, plan, column_annotation):
        return self.strategy.format_generate_code_prompt(self.head_print(df), user_query, plan,
                                                         self.column_description(df),
                                                         self.prepend_col_annotation(column_annotation))

    def generate_code_for_plot_show_prompt(self, df, user_query, plan, column_annotation):
        return self.strategy.format_generate_code_for_plot_show_prompt(self.head_print(df), user_query, plan,
                                                                       self.column_description(df), self.prepend_col_annotation(column_annotation))

    def generate_code_for_plot_save_prompt(self, df, user_query, plan, save_plot_name="", column_annotation=""):
        return self.strategy.format_generate_code_for_plot_save_prompt(self.head_print(df), user_query, plan,
                                                                       self.column_description(df),
                                                                       save_plot_name=save_plot_name, column_annotation=self.prepend_col_annotation(column_annotation))

    def fix_code_prompt(self, df, user_query, code_to_be_fixed, error_message, initial_coder_prompt, column_annotation):
        return self.debug_strategy.format(code=code_to_be_fixed, df_head=self.head_print(df), error=error_message,
                                          input=user_query, head_number=self.head_number, column_description=self.column_description(df),
                                          initial_coder_prompt=initial_coder_prompt,
                                          col_annotation=Prompts.prepend_col_annotation(column_annotation))
