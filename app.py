from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os
from PIL import Image
import pdf2image
import io
import base64

load_dotenv()

genai.configure(api_key =os.getenv("GOOGLE_API_KEY"))

def get_gemini_content(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts =[
            {
                "mime_type":"image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title = 'Resume Checker')
st.header("ATS tracking system")
input_text = st.text_area("Job Description: ",key='input')
uploaded_file = st.file_uploader("Upload your resume(PDF)....",type = ['PDF'])
if uploaded_file is not None:
    st.write("PDF uploded successfully")

submit1 = st.button("Tell Me About the Resume")
# submit2 = st.button("How Can I Improvise my Skills")
submit2 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Data Analyst and Business Analyst, 
your task is to review the provided resume 
against the job description for these profiles.
Please share your professional evaluation on wheather the candidate's profile aligns with the role.
Highlights the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a skilled ATS (Application Tracking System) scanner with a deep understanding of 
Data Science, Data Analyst, Business Analyst and deep ATS functionality
your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the reume matches with job description.
First the output should as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_content(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_content(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
