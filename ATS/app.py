import PyPDF2 as pdf
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3, json
import os
import streamlit as st

load_dotenv() ## load all our environment variables

os.environ["AWS_PROFILE"] = "sidrik-iam"

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

modelID = "ai21.j2-ultra-v1"

llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"temperature":0.1,"maxTokens":8191}
)

def my_chatbot(input):
    prompt = PromptTemplate(
        input_variables=["input"],
        template="You are a chatbot having {input}"
    )
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    response=bedrock_chain({'input':input})
    return response['text']

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering, cloud and devops. 
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the below structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=my_chatbot(input_prompt)
        st.subheader(response)