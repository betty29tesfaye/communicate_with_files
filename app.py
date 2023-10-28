import streamlit as st
uploaded_file = st.file_uploader('Upload a file')
if uploaded_file is not None:
  st.write("file uploaded")
