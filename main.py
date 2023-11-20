import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = 'Tpfr10TXks2NTRlsezAdT3BlbkFJkwjUdMwgojFKFsQrrGDH'

def load_files():
    text = ""
    data_dir = os.path.join(os.getcwd(), "data")
    for filename in os.listdir(data_dir):
        if filename.endwith(".txt"):
            with open(os.path.join(data_dir, filename), "r") as f:
                text += f.read()
    return text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    raw_text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
        
    return raw_text


def get_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {   
                    "role": "system",
                    "content": prompt,
                },
            ],
        )
    return response.choices[0].message.content.strip()

def main():
    
    st.title("Summarizer App")
    st.divider()

    option = st.radio("Select Input type", ("Text", "PDF"))

    if option == "Text":
        user_input = st.text_area("Enter Text", "")

        if st.button("Summarize") and user_input != "":
            response = get_response(user_input)
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please Enter Text.")
    
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if st.button("Summary") and uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)

            response = get_response(text=text)
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please Upload a PDF File.")

if __name__ == "__main__":
    main()
