from multiprocessing import process
import streamlit as st
import random
import time
from genai_center_integration import GenAICenterLLM
from sql_chain import sql_query_chain
import dotenv
import os
from time import process_time_ns

# Automatically loads in api_key from environment of user, user must specify variable in their environment
dotenv.load_dotenv(dotenv.find_dotenv())
api_key = os.environ.get("OPENAI_API_KEY")
# Creates UI model sidebar
model = st.sidebar.selectbox("Which LLM Model?", ("gpt-3.5-turbo", "gpt-3.5-turbo-0301"))

# Called when the user inputs a question as input_text and hits enter into search bar
def generate_response(input_text):
    start_time = process_time_ns()
    print(start_time)
    print("INPUT: ", input_text)
    print("MODEL: ", model)
    # Calls the sql_query_chain function with the updated conversation messages, and defined model from sidebar
    response_query, response_status = sql_query_chain(input_text, st.session_state.messages, model, api_key)
    print("RESPONSE QUERY: ", response_query)
    elapsed_time = process_time_ns() - start_time
    print("elapsed time: ", elapsed_time)
    return response_query, response_status, elapsed_time
    # You see these responses that are returned reflected in the UI

st.title("GenAI Cohort 3 - SQL")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["status"] == "success":
            body = "✅" + "\t" + str(message["llm_time"]) + "ns" + "\t" + str(message["llm_model"])
            st.caption(body)
        elif message["status"] == "failure":
            body = "❌" + "\t" + str(message["llm_time"]) + "ns" + "\t" + str(message["llm_model"])
            st.caption(body)
        else:
            pass

# Accept user input
if prompt := st.chat_input("How can I assist you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "llm_model": model, "status": "none", "llm_time": None})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Generate response based on prompt from user
        assistant_response, response_status, response_time = generate_response(prompt)
        # st.markdown(assistant_response_query)
        st.markdown(assistant_response)
        if response_status == True:
            st.session_state.messages.append({"role": "assistant", "content": assistant_response, "llm_model": model, "status": "success", "llm_time": response_time})
            caption_body = "✅" + "\t" + str(response_time) + "ns" + "\t" + str(model)
            st.caption(caption_body)
        else:
            st.session_state.messages.append({"role": "assistant", "content": assistant_response, "llm_model": model, "status": "failure", "llm_time": response_time})
            caption_body = "❌" + "\t" + str(response_time) + "ns" + "\t" + str(model)
            st.caption(caption_body)

