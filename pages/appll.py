import streamlit as st
import requests
st.markdown("<h1 style='text-align: left;'>Face Paralysis Classification</h1>", unsafe_allow_html=True)
uploaded_files = st.sidebar.file_uploader(
    "Upload files for prediction",
    type=["png", "jpg"], accept_multiple_files=True)
if uploaded_files:
    # Sort files alphabetically by file name
    uploaded_files = sorted(uploaded_files, key=lambda x: x.name)
    if len(uploaded_files) % 2 == 0:  # Ensure there's an even number of files
        for i in range(0, len(uploaded_files), 2):
            file1 = uploaded_files[i]
            file2 = uploaded_files[i + 1]
            col1, col2 = st.columns([1, 1])  # Two columns for each pair of images
            url = 'https://strokediag-xwy6mzfeuq-wn.a.run.app/uploadfile/'
            # Process and display the first image in the first column
            with col1:
                st.image(file1, width=240)
            with col2:
                st.image(file2, width=240)
            # Process and display the first image in the first column
            with col1:
                # st.image(file1, width=240)
                files = {'file': (file1.name, file1, file1.type)}
                response_file1 = requests.post(url, files=files)
                if response_file1.status_code == 200:
                    prediction_file1 = response_file1.json().get('prediction')
                    result_text1 = "No Face Paralysis" if prediction_file1 == 0 else "Face Paralysis Detected"
                    color1 = "green" if prediction_file1 == 0 else "red"
                    st.markdown(f"<h4 style='text-align: left; color: {color1};'>{result_text1}</h4>", unsafe_allow_html=True)
                else:
                    st.error('Error with First Image:', response_file1.text)
            # Process and display the second image in the second column
            with col2:
                # st.image(file2, width=240)
                files = {'file': (file2.name, file2, file2.type)}
                response_file2 = requests.post(url, files=files)
                if response_file2.status_code == 200:
                    prediction_file2 = response_file2.json().get('prediction')
                    result_text2 = "No Face Paralysis" if prediction_file2 == 0 else "Face Paralysis Detected"
                    color2 = "green" if prediction_file2 == 0 else "red"
                    st.markdown(f"<h4 style='text-align: left; color: {color2};'>{result_text2}</h4>", unsafe_allow_html=True)
                else:
                    st.error('Error with Second Image:', response_file2.text)
