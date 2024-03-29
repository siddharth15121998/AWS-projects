
####THIS IS NOT RAG BASED MODEL. IT GIVES Outdated data.#################

from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3, json
import os
import streamlit as st

os.environ["AWS_PROFILE"] = "sidrik-iam"

#bedrock client
# python3 -m streamlit run chatbot.py 

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

modelID = "ai21.j2-ultra-v1"


llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"temperature":1}
)

def my_chatbot(language,freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in {language}.\n\n{freeform_text}"
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)

    response=bedrock_chain({'language':language, 'freeform_text':freeform_text})
    return response

print(my_chatbot("english","who is Virat Kohli?"))

# st.title("Bedrock Chatbot")

# language = st.sidebar.selectbox("Language", ["english", "Spanish"])

# if language:
#     freeform_text = st.sidebar.text_area(label="what is your question?",
#     max_chars=100)

# if freeform_text:
#     response = my_chatbot(language,freeform_text)
#     st.write(response['text'])



    
