import streamlit as st
import requests

st.title('File Upload to FastAPI')

uploaded_file = st.file_uploader("Choose a file (e.g., a44.png)")

if uploaded_file is not None:
    # Show details of the file
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write(file_details)

    # url = 'http://localhost:8000/uploadfile/'  # Replace with your FastAPI URL
    # Send the file to FastAPI server
    url = 'https://strokediag-xwy6mzfeuq-wn.a.run.app/uploadfile/'
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(url, files=files)

    # Show the response from the server
    if response.status_code == 200:
        st.success('File successfully uploaded and processed.')
        st.json(response.json())
    else:
        st.error('An error occurred during upload.')
        st.write('Status code:', response.status_code)
        st.write('Response body:', response.text)
