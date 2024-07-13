import streamlit as st
import pandas as pd
import plotly.express as px
import tempfile
import os
import io


#FUNTIONS HERE:

#excel combiner for sem 1 and 2 
def combine_excel(file1, file2):
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')
    #dropping the header (f2)  here 
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df


























#the page
st.set_page_config(page_title="Report Automator")
st.title("NPTEL Report Generator")
st.write("V 1.1.0")


#file uploader. using 2 as to seperate sem 1 and 2. (may change later)
uploaded_file1 = st.sidebar.file_uploader("Upload first Excel file", type=["xlsx", "xls"])
uploaded_file2 = st.sidebar.file_uploader("Upload second Excel file", type=["xlsx", "xls"])

#sucessful upload
if uploaded_file1 is not None and uploaded_file2 is not None:
    st.write("Upload sucessful!")
    with st.expander("Academic year data: "):
        combined_df = combine_excel(uploaded_file1, uploaded_file2)
        st.write(combined_df)
    
else:
    st.write("upload two files")



