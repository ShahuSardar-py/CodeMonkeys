import streamlit as st
import pandas as pd
import plotly.express as px

# Functions here:

# Excel combiner for sem 1 and 2 
def combine_excel(file1, file2):
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df

def drop_columns(df, columns_to_drop):
    return df.drop(columns=columns_to_drop, errors='ignore')

def role_filter(df):
    faculty_df = df[df['Role'] == 'faculty']
    student_df = df[df['Role'] == 'student']
    return faculty_df, student_df

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

def dept_histogram(df, column):
    fig = px.bar(df, x=column, title=f'Histogram of {column}')
    st.plotly_chart(fig)

# The page
st.set_page_config(page_title="Report Automator")
st.title("NPTEL Report Generator")
st.write("V 1.1.0")

# File uploader. Using 2 to separate sem 1 and 2.
uploaded_file1 = st.sidebar.file_uploader("Upload first Excel file", type=["xlsx", "xls"])
uploaded_file2 = st.sidebar.file_uploader("Upload second Excel file", type=["xlsx", "xls"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    st.write("Upload successful!")
    
    
    st.markdown("----")
    st.write("# Analysis Report")

    summary_df = summary(faculty_df, student_df)
    st.write("#### Summary Statistics")
    st.write(summary_df)

    st.write("#### Department Histogram")
    dept_histogram(combined_df, "Department")

    department_counts = combined_df['Department'].value_counts().reset_index()
    department_counts.columns = ['Department', 'Count']
    max_count = department_counts['Count'].max()


else:
    st.write("Please upload two files")



#EXTRA DATA 
#def combine_file(files):
#    combined_df = pd.DataFrame()
#    for i, file in enumerate(files):
#        df = pd.read_excel(file)
#       if i > 0:
#            df.columns = combined_df.columns  
#        combined_df = pd.concat([combined_df, df], ignore_index=True)
#   return combined_df

#file uplaoder in the sidebar

#files = st.sidebar.file_uploader(
#    "Upload the result files",
#    accept_multiple_files=True,
#    type=["xlsx", "xls"]
#


#if files:
#    for file in files:
#        file_container = st.expander(
#            f"File name: {file.name} ({file.size})"
#        )
#        data = io.BytesIO(file.getbuffer())
#       df = pd.read_excel(data, engine='openpyxl')
#        file_container.write(df)

#    st.write("upload success!")
#    combined_df = combine_file(files)