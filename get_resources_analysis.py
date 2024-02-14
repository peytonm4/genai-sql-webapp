from llm_cost_estimation import models


def token_analysis(token_list: dict[str, int], llm_model_name: str):
    """this function will calculate tokens and cost for the prompt and completion and write them to a text file"""
    for model_name in models:
        if model_name["name"] == llm_model_name:
            print(f'Model Name: {model_name["name"]}')
            print(f'Completion Tokens: {token_list["completion_tokens"]}')
            print(f'Prompt Tokens: {token_list["prompt_tokens"]}')
            print(f'Completion Cost Per Token: {model_name["completion_cost_per_token"]}')
            print(f'Prompt Cost Per Token: {model_name["prompt_cost_per_token"]}')
            print(f'Completion Total Cost: {eval(model_name["completion_cost_per_token"])*token_list["completion_tokens"]}')
            print(f'Prompt Total Cost: {eval(model_name["prompt_cost_per_token"])*token_list["prompt_tokens"]}')
            print(f'Maximum Tokens: {model_name["max_tokens"]}')
            print(f'Description: {model_name["description"]}')

            file1 = open("Model_Performance.txt", "a")
            file1.write('  ')
            file1.writelines(f'Model Name: {model_name["name"]}')
            file1.write('  ')
            file1.writelines(f'Completion Tokens: {token_list["completion_tokens"]}')
            file1.write('  ')
            file1.writelines(f'Prompt Tokens: {token_list["prompt_tokens"]}')
            file1.write('  ')
            file1.writelines(f'Completion Cost Per Token: {model_name["completion_cost_per_token"]}')
            file1.write('  ')
            file1.writelines(f'Prompt Cost Per Token: {model_name["prompt_cost_per_token"]}')
            file1.write('  ')
            file1.writelines(f'Completion Total Cost: {eval(model_name["completion_cost_per_token"])*token_list["completion_tokens"]}')
            file1.write('  ')
            file1.writelines(f'Prompt Total Cost: {eval(model_name["prompt_cost_per_token"])*token_list["prompt_tokens"]}')
            file1.write('  ')
            file1.writelines(f'Maximum Tokens: {model_name["max_tokens"]}')
            file1.write('  ')
            file1.writelines(f'Description: {model_name["description"]} ')
            file1.write(' ------------------------------------------------------------------------------------------------------------------------ ')
            file1.close()


