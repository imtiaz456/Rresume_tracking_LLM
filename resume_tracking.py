from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
from pdf2image import convert_from_path 
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input, pdf_content,prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_files):
    if uploaded_file is not None:
        ##Convert the pdf into image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        # FIRST image will be the entire content of the pdf
        first_page = images[0]
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        #### Add the encoded image to the list
        pdf_parts = [
        {   "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode() ## encode to base64
        }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


################# Streamlit app ################

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type =["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded successfully")

submit1 =  st.button("Tell me about your resume")
# submit2 = st.button("How can i improvise our skills")
submit3 = st.button("Percentage match")

# for shortlisting resumes.


input_prompt1 = """
You are an experienced HR with Tech experince in the field of any one job from role Data science,Full stack web development,Big data engineering, DevOps, Data Analyst,
your task is to review the provided resume against the job description for these profiles.
please share your professional evaluations on whether the candidate's profile aligns with the role.
Highlights the strengths and weeknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of any one job role in Data science,Full stack web development,Big data engineering,
DevOps, Data Analyst and deep ATS functionality, your task is to evaluate the resume against the provided job description. Give me the
percentage of match if the resume matches the job description. First the output should come as percentage and then keyword missing and last
final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")