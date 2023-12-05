import streamlit as st
import requests
import os

st.title('File Upload to FastAPI')

uploaded_file = st.file_uploader("Choose a file (e.g., a44.png)")

if uploaded_file is not None:
    # Show details of the file
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write(file_details)

    # Save the file to a temporary location
    if not os.path.exists('tempDir'):
        os.mkdir('tempDir')
    temp_file_path = os.path.join('tempDir', uploaded_file.name)

    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Send the file to FastAPI server
    url = 'http://localhost:8000/uploadfile/'  # Replace with your FastAPI URL
    with open(temp_file_path, 'rb') as f:
        files = {'file': (uploaded_file.name, f)}
        response = requests.post(url, files=files)

    # Remove the file after upload
    os.remove(temp_file_path)

    # Show the response from the server
    if response.status_code == 200:
        st.success('File successfully uploaded and processed.')
        st.json(response.json())
    else:
        st.error('An error occurred during upload.')
        st.write('Status code:', response.status_code)
        st.write('Response body:', response.json())
