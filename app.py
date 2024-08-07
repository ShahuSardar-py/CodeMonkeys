import streamlit as st
import pandas as pd
import plotly.express as px
from preprocessor import preprocess_data

#funtions
def value_counter(df: pd.DataFrame, column: str, value: str) -> int:
    return df[column].value_counts().get(value, 0)


def course_info(df, column):
    return df[column].value_counts()

























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

    # # combined dataframe here (with expander)
    # with st.expander("Combined Academic Year Data"):
    #     st.write(combined_df)

    # # Display faculty DataFrame
    # with st.expander("Faculty Data"):
    #     st.write(faculty_df)

    # # Display student DataFrame
    # with st.expander("Student Data"):
    #     st.write(student_df)

    with st.expander("main DATA"):
        st.write(main_df)

    # Display summary statistics
    # summary_data = {
    #     'Role': ['Faculty', 'Student'],
    #     'Count': [len(faculty_df), len(student_df)],
    #     'Elite Certificate': [
    #         (faculty_df['Certificate Type'] == 'elite').sum(),
    #         (student_df['Certificate Type'] == 'elite').sum()
    #     ],
    #     'Elite+Silver Certificate': [
    #         (faculty_df['Certificate Type'] == 'elite+silver').sum(),
    #         (student_df['Certificate Type'] == 'elite+silver').sum()
    #     ],
    #     'Average Exam Score': [
    #         faculty_df['Exam Score'].mean(),
    #         student_df['Exam Score'].mean()
    #     ]
    # }
    # summary_df = pd.DataFrame(summary_data)
    # st.write("### Summary Statistics")
    # st.write(summary_df)

    # Display Plotly histogram for "Department"
    
    # 
    
    f_no= value_counter(main_df, 'Role', 'faculty')
    s_no=value_counter(main_df, 'Role', 'student')
    total_count= (f_no)+(s_no)

    

    st.write("# Report Analysis")

    
    col1, col2, col3= st.columns(3)
    with col1:
        st.header("Total")
        st.title(total_count)
    with col2:
        st.header("faculty")
        st.title(f_no)
        

    with col3:
        st.header("students")
        st.title(s_no)
    





    elite_faculty= (faculty_df['Certificate Type'] == 'Elite').sum()
    elite_student= (student_df['Certificate Type'] == 'Elite').sum()
    ES_faculty= (faculty_df['Certificate Type'] == 'Elite+Silver').sum()
    ES_student=(student_df['Certificate Type'] == 'Elite+Silver').sum()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("### Elite (faculty)")
        st.title(elite_faculty)
    with col2:
        st.write("### Elite (student)")
        st.title(elite_student)
    with col3:
        st.write("### Elite + Silver (faculty)")
        st.title(ES_faculty)
    with col4:
        st.write("### Elite+Silver (student)")
        st.title(ES_student)
        

    
        

    
    
    fig = px.histogram(main_df, x="Department", title='Histogram of Department')
    st.plotly_chart(fig)
    
    summary_data = {
        'Role': ['Faculty', 'Student'],
        'Count': [len(faculty_df), len(student_df)],
        'Elite Certificate': [
            (faculty_df['Certificate Type'] == 'Elite').sum(),
            (student_df['Certificate Type'] == 'Elite').sum()
        ],
        'Elite+Silver Certificate': [
            (faculty_df['Certificate Type'] == 'Elite+Silver').sum(),
            (student_df['Certificate Type'] == 'Elite+Silver').sum()
        ]
         
        }
    summary_df = pd.DataFrame(summary_data)
    st.write("### Certifications")
    st.write(summary_df)




    course_counts = course_info(main_df, 'Course Name')
    
    # Prepare data for pie chart
    top_3 = course_counts.head(3)
    other_count = course_counts.iloc[3:].sum()
    pie_data = top_3._append(pd.Series({'Other': other_count}))
    
    # Display pie chart for top 3 courses
    
    pie_chart = px.pie(pie_data, values=pie_data.values, names=pie_data.index, title='Top Most courses')
    st.plotly_chart(pie_chart)

else:
    st.write("Please upload the files")
