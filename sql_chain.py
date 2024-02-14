from langchain.chains import create_sql_query_chain
from langchain.sql_database import SQLDatabase
from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import ChatPromptTemplate
# from get_resources_analysis import num_tokens_from_string
from parse_for_output import parse_final_answer, parse_final_answer_from_ai
from custom_llm import CustomLLM
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


def sql_query_chain(prompt, messages, llm_model, api_key):
    # Use SQlite to tag to database
    db = SQLDatabase.from_uri("sqlite:///movie_titles.db")
    #Build the llm variable using the CustomLLM langchain wrapper, pass in the model and api_key strings
    llm = CustomLLM(model=llm_model, api_key=api_key)
    # Define the system template that will be inserted into the prompt template
    # This will instruct the LLM how to operate and answer the request
    system_template = """You are a {dialect} expert. Given an input question, create a syntactically correct {dialect} query to run.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Only use the following tables:
{table_info}

Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

Use format:

Final answer: <<FINAL_ANSWER_QUERY>>"""
    # Define the llm_input variable pulling in the question that is invoked with the sql_query_chain as prompt
    llm_input = {
        "question": prompt
    }

    # The prompt template sets up a template that langchain understands, defining how LLM should operate
    # This is based off of information that langchain pulls from the database
    prompt_template = ChatPromptTemplate.from_messages([("system", system_template)]).partial(
        dialect=db.dialect,
        table_info=db.get_table_info())
    
    # This serves to track the conversation history, continously appending the users messages to the overall message content
    # We define the question and response using HumanMessage and AI Message differentiators
    for message in messages:
        if message["role"] == "user":
            prompt_template.messages.append(HumanMessage(content=message["content"]))
        if message["role"] == "assistant":
            prompt_template.messages.append(AIMessage(content=message["content"]))
    
    # Here we create a chain that runs on the database defined at the beginning of the function
    # Each time this sql_query_chain function is called, it defines the llm being used, the database, and appends any additional messages to the prompt template
    # Then it creates a new db_chain with this info where the langchain create_sql_query_chain function is called - then its final answer is parsed from the output
    db_chain = create_sql_query_chain(llm, db, prompt=prompt_template) | parse_final_answer
    # Chain references the database - formats the messages appropriately - then calls the Custom LLM
    # The CustomLLM wrapper calls the GenAI Center LLM which receives post a request and receives output from Gen AI Center API
    # This output is parsed for its final answer - the query needed to find the data requested
    try:
        db_query = db_chain.invoke(llm_input)
        print(db_query)
    except:
        return "Chain invocation unsuccessful", False
    # This query is then ran on the database, to find the exact answer requested by the user
    try:
        db_query_response = db.run(db_query)
    except:
        return "Query exectuion unsuccessful", False

    # An answer prompt formats the resulting data for the user in a humanlike response
    answer_prompt = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Result: {result}
Answer: """
    
    answer_prompt_template = ChatPromptTemplate.from_messages([("system", answer_prompt)]).partial(result=db_query_response)

    for message in messages:
        if message["role"] == "user":
            answer_prompt_template.messages.append(HumanMessage(content=message["content"]))
        if message["role"] == "assistant":
            answer_prompt_template.messages.append(AIMessage(content=message["content"]))

    print(answer_prompt_template)

    # We then format the answer by updating the answer information into the answer template
    # The llm is called with this information, goes through the process outlined above
    # The desired response is parsed from the output 
    answer_chain = answer_prompt_template | llm | parse_final_answer_from_ai
    # answer_chain = answer_prompt_template | llm | StrOutputParser()    

    answer_response = answer_chain.invoke({"question": prompt})
    print(answer_response)



    return answer_response, True
