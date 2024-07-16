from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format='JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
           {
               "mime_type": "image/jpeg",
               "data": base64.b64encode(image_byte_arr).decode()
           }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS resume Expert")
st.header("ATS tracking System")
input_text=st.text_area("Job description:",key="input")
uploaded_file=st.file_uploader("upload your resume",type=["pdf"])


if uploaded_file is not None:
    st.write("file iloaded successfully")

submit1=st.button("Tell me about your resume")

submit3=st.button("Percentage Match")

input_prompt1="""You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""
input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("please upload the resume")
