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
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df

#faculty and student diffrentiator
def role_filter(df):
    faculty_df = df[df['Role'] == 'faculty']
    student_df = df[df['Role'] == 'student']
    return faculty_df, student_df

#column drop
def drop_columns(df, columns_to_drop):
    return df.drop(columns=columns_to_drop, errors='ignore')


#summary table
def summary(faculty_df, student_df):
    summary_data = {
        'Role': ['Faculty', 'Student'],
        'Elite + Silver': [
            (faculty_df['Certificate Type'] == 'Elite+Silver').sum(),
            (student_df['Certificate Type'] == 'Elite+Silver').sum()
        ],
        'Elite Certificate': [
            (faculty_df['Certificate Type'] == 'Elite').sum(),
            (student_df['Certificate Type'] == 'Elite').sum()
        ],
        'Successfully completed': [
            (faculty_df['Certificate Type'] == 'Successfully completed').sum(),
            (student_df['Certificate Type'] == 'Successfully completed').sum()
        ],
        'No Certificate': [
            (faculty_df['Certificate Type'] == 'No Certificate').sum(),
            (student_df['Certificate Type'] == 'No Certificate').sum()
        ],
        'Average Exam Score': [
            faculty_df['Final Score'].mean(),
            student_df['Final Score'].mean()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    return summary_df




















#the page setup (UI)
st.set_page_config(page_title="Report Automator")
#header
st.title("NPTEL Report Generator")
st.write("V 1.1.0")


#file uploader. using 2 as to seperate sem 1 and 2. (may change later)
uploaded_file1 = st.sidebar.file_uploader("Upload first Excel file", type=["xlsx", "xls"])
uploaded_file2 = st.sidebar.file_uploader("Upload second Excel file", type=["xlsx", "xls"])

#sucessful upload
if uploaded_file1 is not None and uploaded_file2 is not None:
    st.write("Upload successful!")
    combined_df = combine_excel(uploaded_file1, uploaded_file2)
    
    columns_to_drop = ["College Roll no", "Unproctored programming exam score out of 25", "Year of passing"]
    combined_df = drop_columns(combined_df, columns_to_drop)
    
    faculty_df, student_df = role_filter(combined_df)
    
    with st.expander("Faculty Data"):
        st.write(faculty_df)

    with st.expander("Student Data"):
        st.write(student_df)
    
    st.markdown("----")
    st.write("# Analysis Report")

    summary_df = summary(faculty_df, student_df)
    st.write("#### Summary Statistics")
    st.write(summary_df)

    


else:
    st.write("Please upload two files")



