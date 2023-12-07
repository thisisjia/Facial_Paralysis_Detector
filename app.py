import streamlit as st
import requests

st.title('Stroke Prediction')
uploaded_files = st.sidebar.file_uploader("Upload pairs of files (e.g., nostroke_01.png, stroke_01.png)",
    type=["png", "jpg"], accept_multiple_files=True)

# Check if files were uploaded and there's an even number for pairs
if uploaded_files and len(uploaded_files) % 2 == 0:
    # Iterate over the files in pairs
    for i in range(0, len(uploaded_files), 2):
        nostroke_file = uploaded_files[i]
        stroke_file = uploaded_files[i + 1]

        # Display each pair of images
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(nostroke_file, caption='No Stroke', use_column_width=True)
        with col2:
            st.image(stroke_file, caption='Stroke', use_column_width=True)

        # Send the files to FastAPI server for prediction
        url = 'https://strokediag-xwy6mzfeuq-wn.a.run.app/uploadfile/'

        # Predict for 'No Stroke'
        files = {'file': (nostroke_file.name, nostroke_file, nostroke_file.type)}
        response_nostroke = requests.post(url, files=files)

        # Predict for 'Stroke'
        files = {'file': (stroke_file.name, stroke_file, stroke_file.type)}
        response_stroke = requests.post(url, files=files)

        # Show the prediction result
        with col3:
            st.write("Predicted Results:")
            if response_nostroke.status_code == 200 and response_stroke.status_code == 200:
                # Assuming the response contains the prediction result as {'prediction': 0 or 1}
                prediction_nostroke = response_nostroke.json().get('prediction')
                prediction_stroke = response_stroke.json().get('prediction')

                # Determine if the predictions are incorrect
                nostroke_incorrect = (prediction_nostroke != 0)
                stroke_incorrect = (prediction_stroke != 1)

                # Highlight incorrect predictions
                if nostroke_incorrect:
                    st.markdown(f"<span style='color: red'>**Before Stroke Prediction: Stroke**</span>", unsafe_allow_html=True)
                else:
                    st.write("Before Stroke Prediction: No Stroke")

                if stroke_incorrect:
                    st.markdown(f"<span style='color: red'>**After Stroke Prediction: No Stroke**</span>", unsafe_allow_html=True)
                else:
                    st.write("After Stroke Prediction: Stroke")
            else:
                st.error(f'An error occurred during predictions.')
                if response_nostroke.status_code != 200:
                    st.write('No Stroke Image Error:', response_nostroke.text)
                if response_stroke.status_code != 200:
                    st.write('Stroke Image Error:', response_stroke.text)
elif uploaded_files and len(uploaded_files) % 2 != 0:
    st.warning("Please upload the images in pairs for prediction.")
else:
    st.warning("Please upload the image files for prediction.")
