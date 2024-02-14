# SQL Generation using Langchain & OpenAI
This code repository starts up a Generative AI application using Large Language Models (LLM) that can generate SQL Queries, and subsequently answer those queries. It responds to user input in a conversational manner, stores conversation history, and handles error edge cases.

# How does the user interact with the application?
This use case is ideal for individuals and businesses to help Data Analysts accelerate query development , improve productivity, and save time and resources. The Data Analyst (user) ineracts with a front end design on Streamlit. They can choose between two models offered through the Deloitte Generative AI center: GPT-3.5-Turbo & GPT-3.5-Turbo-0301. The user can select their desired model from the model dropdown bar on the top left and then insert the intent of the query by providing text based prompts. The application should be able to produce the SQL Query and subsequent answer. 

# Key Aspects of the Code
1. API Key: In order to access the LLM API, an API key will be required. This key will
be used to authenticate the user and ensure that they have the necessary permissions to
access the API. It is important to keep the API key secure.
2. Lang Chain: This is a framework that encapsulates most aspects of using LLMs and
helps create LLM driven applications.
3. Session Management : To maintain proper session management, an in-memory cache is used. The cache will store session data in memory, making it faster and more efficient than storing the data in a database. This
will help to ensure that the conversation with the user is seamless and that the user's progress is tracked accurately.

# How to start up the SQL Gen Application
## Docker
Docker is the preferred deployment method as it offers repeatable build pipelines.  Below is a quickstart on how to achieve that.
1. Build the image locally.  You need to be in the directory where the Dockerfile is located.
```shell
~/ docker build -t streamlit .
```
2. Start the container to listen on port 8501.  This runs the application in the foreground where you can also see relevant logging details.
```shell
~/ docker run -it --rm -p 127.0.0.1:8501:8501 streamlit
```
3. Open a new browser and navigate to `http://localhost:8501` to access the application.

## Run in browser
1. Access the requirements.txt  file, ensure that the folder you are operating in has the appropriate versioning and modules
2. Type in python3 streamlit -m run streamlit_web.py into terminal to start up streamlit and run in your browser. You can now ask questions regarding the movies_titles database
3. Additionally, you can use the sql_setup.py file to structure your own database or bring in online database from url using sqlite

# A step by step guide for the user to understand each file
## Extraneous files
### movie_titles.db
This is a database that can be used to test the application, you can ask questions regarding the movies in this database, which the application will then develop and execute queries for. 
### sql_setup.py
This file shows how to set up a database for the application, using the sqlite module, the user can pass in their own database or structure using this file.
### requirements.txt
This is a file that outlines the environment in which the user needs to be in in order to run the application. This includes the versioning of various langchain modules.

## Connecting to Generative Ai Center
### genai_center_integration.py
This is Generative AI Center class which connects to the Generative AI Center offered through Deloitte, accesses the LLM's offered at this site, inputs the values passed into the class, and returns the output of these models.
### custom_llm.py
Since the generative center class does not align with the inputs that langchain expects, it is necessary to create a custom LLM wrapper which takes in a prompt string, calls the generative AI center class, receives the output from this class, and formats it with all required attributes to run with langchain. This class is the overarching class which is called within the langchain SQL query chain.
## Using the Langchain framework
### sql_chain.py
This is the sql_query_chain function which sets up and uses the langchain "chain" framework. It creates the database to be accessed and the LLM to be used by langchain. It initializes a prompt using langchains PromptTemplate modules. It initializes session history, where previous messages are stored in memory. Then it executes the chain, and returns the query and the answer derived from executing the query on the database.
### parse_for_output.py
This is a small function built into the sql_chain that parses the final answer from the query response. Seperating the final answer and the query response.
### get_resources_analysis.py
This function evaluates the resources used each time the sql_query_chain is called, and operational metrics associated with the call. It writes these to a text file which can be opend and read by the user.

## Front-end user interaction
How to launch the application, which answers SQL Query questions from your internet browser. 
### streamlit_web.py
This file provides the code for a streamlit web app to run. Upon passing into the terminal:
'''
python3 streamlit -m run streamlit_web.py
'''
It generates responses using the sql_query_chain, handles error cases by outlining whether rephrasing is necessary, and whether a response is received, and has a dropdown for users to switch models.
### Dockerfile
If the user wants to run the application in an image, they can set up the image of the application with the Docker file, and continuously run the file using the Docker engine.
