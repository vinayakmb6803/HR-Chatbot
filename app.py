import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
Hey Act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech field, Software engineering, data science, data analyst and big data engineer. Your task is to evaluate the resume
based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving their resumes. Assign the percentage Matching based on Job Description and the missing Keyword with High Accuracy
Resume:{text}
description:{jd}

I want the response in one single string having the structure 
{{"JD Match" : " % " , "MissingKeywords: []", "Profile Summary" : ""}}
"""

## Streamlit 
st.title("LKQI ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please Upload the Resume")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader(response)