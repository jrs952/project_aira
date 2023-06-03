from keys import openai_key, github_key

from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import LLMChain
from langchain.prompts import PromptTemplate

import streamlit as st

from tools.Tools import setup_tools
from tools.GithubManager import GithubManager
import os

ghMgr = GithubManager(github_key)
tool_list = setup_tools(ghMgr)

llm = OpenAI(openai_api_key=openai_key, temperature=0.7)
agent = initialize_agent(llm, tool_list, agent="zero-shot-react-description", verbose=True)

st.title("LangChain - Github Experiment")
st.info("This is a demo of the LangChain Github Experiment. The goal of this experiment is to create a Github repository with a specified name, and then add a file to it. The repository name and file name are specified by the user, and the file content is generated by the AI. The AI is given a prompt that describes the repository name and file name, and is asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. The AI is then asked to generate a description of the file content. The AI is also given a list of tools that it can use to complete the task. ")


with st.form('my_form'):
    text = st.text_area('Enter a prompt')
    submitted = st.form_submit_button('Submit')

    if submitted:
        result = agent.run(text)
        with st.expander("Show Result"):
            st.info(result)