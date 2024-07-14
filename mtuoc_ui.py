import streamlit as st
import pyperclip 
import sys
import random
import requests
import yaml
import tempfile
import os
import pathlib
import threading
import json
import ast


from translator import translate_segment_MTUOC
from translator import translate
from okapi_docx import OkapiConnector

okapi_connector = OkapiConnector() 

with open("mtSystems.yaml") as stream:
    try:
        mtSystems = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

mt_engine = st.selectbox("Select MT Engine:", mtSystems, format_func=lambda x: x["name"], key="mt_engine_tab1")
ip = mt_engine["ip"]
portMT = mt_engine["port"]
urlMTUOC = f"http://{ip}:{portMT}/translate"

tab1, tab2 = st.tabs(["Text box", "DOCX files"])

with tab1:
    st.header("Translate text")
    
    # Selection list for MT engine

    # Text area for user input
    input_text = st.text_area("Enter text:", help="Enter the text you want to translate")
        
    # Placeholder for translation
    translation = ""

    # Button to trigger translation
    if st.button("Translate"):
        # Call translation function
        translation = translate(input_text,urlMTUOC)

    # Display translation
    translation_text_area=st.text_area("Translation:", value=translation, help="The translation will be shown here")


with tab2:
    st.header("Translate DOCX files")
      
    temp_dir = tempfile.TemporaryDirectory()

    uploaded_file = st.file_uploader(label="Upload a file",type=['doc','docx'])
    if uploaded_file is not None:
        st.write("filename:", uploaded_file.name)
        with open(os.path.join(pathlib.Path(temp_dir.name),uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.lower().endswith(('.doc', '.docx')):
            with st.spinner(text="In progress..."):
                #MTUOCtranslateDOCX(ip,portMT,input_path,output_path, translate_tables=True,translate_headers=True,translate_footers=True,translate_text_boxes=True)
                #MTUOCtranslateDOCX(ip,portMT,os.path.join(pathlib.Path(temp_dir.name),uploaded_file.name),output_file_path)
                output_file_path = okapi_connector.translate(lambda x: translate(x,urlMTUOC),os.path.join(pathlib.Path(temp_dir.name),uploaded_file.name),"en","fi")
            
            with open(output_file_path,'rb') as f:
                st.download_button('Download translated version', f,os.path.basename(output_file_path))
                
            os.remove(output_file_path)
   

