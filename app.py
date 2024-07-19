import streamlit as st
import pandas as pd
import plotly.express as px
from preprocessor import preprocess_data

# APP UI 
st.set_page_config(page_title="Report Automator")
st.title("NPTEL Report Generator")
st.write("V 1.2.0")

# SIDE BAR 
uploaded_files = st.sidebar.file_uploader(
    "Upload the result files",
    accept_multiple_files=True,
    type=["xlsx", "xls"]
)

# for successful upload
if uploaded_files:
    st.write("Upload successful!")
    
    # preprocessor module function from module 
    combined_df, cleaned_df, main_df, absent_df, faculty_df, student_df = preprocess_data(uploaded_files)

    # combined dataframe here (with expander)
    with st.expander("Combined Academic Year Data"):
        st.write(combined_df)

    # Display faculty DataFrame
    with st.expander("Faculty Data"):
        st.write(faculty_df)

    # Display student DataFrame
    with st.expander("Student Data"):
        st.write(student_df)

    with st.expander("Main Data (Present Entries Only)"):
        st.write(main_df)

    # Display summary statistics
    summary_data = {
        'Role': ['Faculty', 'Student'],
        'Count': [len(faculty_df), len(student_df)],
        'Elite Certificate': [
            (faculty_df['Certificate Type'] == 'elite').sum(),
            (student_df['Certificate Type'] == 'elite').sum()
        ],
        'Elite+Silver Certificate': [
            (faculty_df['Certificate Type'] == 'elite+silver').sum(),
            (student_df['Certificate Type'] == 'elite+silver').sum()
        ],
        'Average Exam Score': [
            faculty_df['Exam Score'].mean(),
            student_df['Exam Score'].mean()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    st.write("### Summary Statistics")
    st.write(summary_df)

    # Display Plotly histogram for "Department"
    st.write("### Department Histogram")
    fig = px.histogram(main_df, x="Department", title='Histogram of Department')
    st.plotly_chart(fig)
else:
    st.write("Please upload the files")
